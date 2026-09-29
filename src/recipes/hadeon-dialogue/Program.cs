using Andre.Formats;
using SoulsFormats;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text.Json;

// Build a guarded TalkParam-only candidate. Never overwrite source, runtime or editor files.
if (args.Length != 4) throw new ArgumentException("regulation.bin output-directory Smithbox-directory dialogue-manifest.json");
var input = Path.GetFullPath(args[0]);
var output = Path.GetFullPath(args[1]);
var lib = Path.GetFullPath(args[2]);
var manifestPath = Path.GetFullPath(args[3]);
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
AssemblyLoadContext.Default.Resolving += (context, name) => {
    var path = Path.Combine(lib, name.Name + ".dll");
    return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(lib);
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)));
var inputHash = Hash(input);
var manifestHash = Hash(manifestPath);
var manifest = JsonDocument.Parse(File.ReadAllText(manifestPath)).RootElement;
var lines = manifest.GetProperty("lines").EnumerateArray().ToArray();
if (lines.Length != 16 || lines.Select(x => x.GetProperty("index").GetInt32()).Where((x, i) => x != i).Any())
    throw new Exception("Expected exactly sixteen roster-indexed lines");

var regulation = SFUtil.DecryptERRegulation(input);
var member = regulation.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "TalkParam");
var talk = Param.Read(member.Bytes);
var paramdef = PARAMDEF.XmlDeserialize(Path.Combine(lib, "Assets/PARAM/ER/Defs/TalkParam.xml"), true);
talk.ApplyParamdef(paramdef, ulong.Parse(regulation.Version), "TalkParam");
var jsonOptions = new JsonSerializerOptions { IncludeFields = true };
string Row(Param.Row row) => JsonSerializer.Serialize(new { row.ID, row.Name,
    Cells = row.Cells.ToDictionary(c => c.Def.InternalName, c => c.Value) }, jsonOptions);
var beforeRows = talk.Rows.Select(Row).ToArray();
var template = talk.Rows.Single(r => r.ID == 70602000);
int Field(Param.Row row, string name) => Convert.ToInt32(row.Cells.Single(c => c.Def.InternalName == name).Value);
void Set(Param.Row row, string name, int value) {
    var cell = row.Cells.Single(c => c.Def.InternalName == name);
    cell.Value = Convert.ChangeType(value, cell.Value.GetType());
}
if (Field(template, "msgId") != 706020000 || Field(template, "isForceDisp") != 1 ||
    Field(template, "returnPos") != 0 || Field(template, "motionId0") != -1 ||
    Field(template, "motionId1") != -1 || Field(template, "spEffectId0") != -1 ||
    Field(template, "spEffectId1") != -1 || Field(template, "talkAnimationId") != -1)
    throw new Exception("Native TalkParam template changed; review before cloning");

var added = new List<int>();
var retained = new List<int>();
foreach (var line in lines) {
    var index = line.GetProperty("index").GetInt32();
    var baseId = line.GetProperty("talkParamBase").GetInt32();
    var textBase = line.GetProperty("textBase").GetInt32();
    var carrierBase = line.GetProperty("carrierBase").GetInt32();
    var cues = line.GetProperty("cues").EnumerateArray().ToArray();
    if (cues.Length is < 1 or > 10) throw new Exception($"Invalid subtitle count for line {index}");
    for (var cueIndex = 0; cueIndex < cues.Length; cueIndex++) {
        var id = baseId + cueIndex;
        var msgId = textBase + cueIndex * 10;
        var carrierId = carrierBase + cueIndex;
        var text = cues[cueIndex].GetProperty("text").GetString() ?? throw new Exception("Null dialogue text");
        if (index == 0) {
            var existing = talk.Rows.Single(r => r.ID == id);
            if (Field(existing, "msgId") != msgId || Field(existing, "msgId_female") != msgId ||
                Field(existing, "voiceId") != carrierId || Field(existing, "voiceId_female") != carrierId ||
                Field(existing, "isForceDisp") != 0)
                throw new Exception($"Accepted first-entrance TalkParam {id} changed: " +
                    $"name={existing.Name} msg={Field(existing, "msgId")}/{Field(existing, "msgId_female")} " +
                    $"voice={Field(existing, "voiceId")}/{Field(existing, "voiceId_female")} force={Field(existing, "isForceDisp")}");
            // The previously accepted row names held an old draft, though their
            // message IDs already point to the final spoken text.
            existing.Name = "Hadeon: " + text;
            retained.Add(id);
            continue;
        }
        if (talk.Rows.Any(r => r.ID == id)) throw new Exception($"TalkParam {id} is occupied");
        var row = new Param.Row(template) { ID = id, Name = "Hadeon: " + text };
        Set(row, "msgId", msgId);
        Set(row, "msgId_female", msgId);
        Set(row, "voiceId", carrierId);
        Set(row, "voiceId_female", carrierId);
        Set(row, "isForceDisp", 0);
        talk.AddRow(row);
        added.Add(id);
    }
}
member.Bytes = talk.Write();
Directory.CreateDirectory(output);
var candidate = Path.Combine(output, "regulation.bin");
SFUtil.EncryptERRegulation(candidate, regulation, regulation.Compression);
var readback = SFUtil.DecryptERRegulation(candidate);
var baseline = SFUtil.DecryptERRegulation(input);
if (readback.Files.Count != baseline.Files.Count || readback.Version != baseline.Version ||
    readback.Compression != baseline.Compression || readback.Format != baseline.Format ||
    readback.BigEndian != baseline.BigEndian || readback.BitBigEndian != baseline.BitBigEndian ||
    readback.Unicode != baseline.Unicode || readback.Extended != baseline.Extended ||
    readback.Unk04 != baseline.Unk04 || readback.Unk05 != baseline.Unk05)
    throw new Exception("Regulation binder metadata changed");
for (var i = 0; i < baseline.Files.Count; i++) {
    var a = baseline.Files[i]; var b = readback.Files[i];
    if (a.Name != b.Name || a.ID != b.ID || a.Flags != b.Flags || a.CompressionType != b.CompressionType)
        throw new Exception("Regulation member metadata changed");
    if (Path.GetFileNameWithoutExtension(a.Name) != "TalkParam" && !a.Bytes.Span.SequenceEqual(b.Bytes.Span))
        throw new Exception("Unrelated parameter table changed");
}
var talkRead = Param.Read(readback.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "TalkParam").Bytes);
talkRead.ApplyParamdef(paramdef, ulong.Parse(readback.Version), "TalkParam");
if (!talkRead.Rows.Select(Row).SequenceEqual(talk.Rows.Select(Row)))
    throw new Exception("TalkParam readback mismatch");
var baselineTalk = Param.Read(baseline.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "TalkParam").Bytes);
baselineTalk.ApplyParamdef(paramdef, ulong.Parse(baseline.Version), "TalkParam");
var baselineRows = baselineTalk.Rows.ToArray();
foreach (var row in baselineRows.Where(r => retained.Contains((int)r.ID)))
    row.Name = talkRead.Rows.Single(r => r.ID == row.ID).Name;
if (!talkRead.Rows.Take(beforeRows.Length).Select(Row).SequenceEqual(baselineRows.Select(Row)))
    throw new Exception("Existing TalkParam row changed beyond owned Hadeon names");
if (Hash(input) != inputHash || Hash(manifestPath) != manifestHash)
    throw new Exception("Input changed during build");
File.WriteAllText(Path.Combine(output, "validation.json"), JsonSerializer.Serialize(new {
    input, inputHash, manifestPath, manifestHash, candidate, candidateHash = Hash(candidate),
    retainedRows = retained, addedRows = added, preservedOtherTablesAndMetadata = true,
    preservedExistingTalkParamRows = true, gameplayVerified = false
}, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine($"Validated {added.Count} added TalkParam rows, {retained.Count} retained cues; unrelated decoded data preserved.");
