using Andre.Formats;
using SoulsFormats;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text.Json;

// Add a hidden, inert native sound carrier for Hadeon's death voice.
if (args.Length != 4) throw new ArgumentException("regulation.bin map.msb.dcx output-directory Smithbox-directory");
var input = Path.GetFullPath(args[0]);
var mapInput = Path.GetFullPath(args[1]);
var output = Path.GetFullPath(args[2]);
var lib = Path.GetFullPath(args[3]);
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
AssemblyLoadContext.Default.Resolving += (context, name) => {
    var path = Path.Combine(lib, name.Name + ".dll");
    return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(lib);
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)));
var inputHash = Hash(input);
var mapInputHash = Hash(mapInput);

const int carrierEntity = 18002390;
const int carrierNpc = 99989900;
var regulation = SFUtil.DecryptERRegulation(input);
var member = regulation.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "NpcParam");
var def = PARAMDEF.XmlDeserialize(Path.Combine(lib, "Assets/PARAM/ER/Defs/NpcParam.xml"), true);
Param Read(BND4 binder) {
    var table = Param.Read(binder.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "NpcParam").Bytes);
    table.ApplyParamdef(def, ulong.Parse(binder.Version), "NpcParam");
    return table;
}
string Rows(Param table, int? omit = null) => JsonSerializer.Serialize(table.Rows.Where(row => row.ID != omit).Select(row => new {
    row.ID, row.Name, Cells = row.Cells.ToDictionary(c => c.Def.InternalName, c => c.Value)
}));
var table = Read(regulation);
var beforeRows = Rows(table);
if (table.Rows.Any(r => r.ID == carrierNpc)) throw new Exception("Carrier NpcParam ID is occupied");
var template = table.Rows.Single(r => r.ID == 47210070);
int Field(Param.Row row, string name) => Convert.ToInt32(row.Cells.Single(c => c.Def.InternalName == name).Value);
void Set(Param.Row row, string name, int value) {
    var cell = row.Cells.Single(c => c.Def.InternalName == name);
    cell.Value = Convert.ChangeType(value, cell.Value.GetType());
}
if (Field(template, "SoundAddBankId") != -1 || Field(template, "enableSoundObjDist") != -1)
    throw new Exception("Native hidden carrier template changed");
var carrier = new Param.Row(template) { ID = carrierNpc, Name = "Sovereign - Hadeon death sound carrier" };
Set(carrier, "SoundAddBankId", 9998);
Set(carrier, "enableSoundObjDist", 100);
table.AddRow(carrier);
member.Bytes = table.Write();
var talkMember = regulation.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "TalkParam");
var talkDef = PARAMDEF.XmlDeserialize(Path.Combine(lib, "Assets/PARAM/ER/Defs/TalkParam.xml"), true);
Param ReadTalk(BND4 binder) {
    var value = Param.Read(binder.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "TalkParam").Bytes);
    value.ApplyParamdef(talkDef, ulong.Parse(binder.Version), "TalkParam");
    return value;
}
var talk = ReadTalk(regulation);
var talkRow = talk.Rows.Single(r => r.ID == 99980001);
if (talkRow.Name != "Hadeon: Ancient is mine oath." ||
    Field(talkRow, "msgId") != 999800010 || Field(talkRow, "voiceId") != 999800011)
    throw new Exception("First-entrance TalkParam baseline changed");
talkRow.Name = "Hadeon: Long have I kept mine oath.";
talkMember.Bytes = talk.Write();

var map = MSBE.Read(mapInput);
var nativePart = map.Parts.Enemies.Single(p => p.EntityID == 18000852);
var hadeon = map.Parts.Enemies.Single(p => p.EntityID == 18002354);
if (nativePart.NPCParamID != 47210070 || nativePart.TalkID != 0 || nativePart.ModelName != "c4721" ||
    hadeon.NPCParamID != 25000011 || map.Parts.GetEntries().Any(p => p.EntityID == carrierEntity))
    throw new Exception("Map actor baseline or carrier ID changed");
var newPart = (MSBE.Part.Enemy)nativePart.DeepCopy();
newPart.Name = "c4721_9900";
newPart.EntityID = carrierEntity;
newPart.NPCParamID = carrierNpc;
newPart.Position = hadeon.Position;
newPart.Rotation = hadeon.Rotation;
map.Parts.Enemies.Add(newPart);

Directory.CreateDirectory(output);
var regulationCandidate = Path.Combine(output, "regulation.bin");
var mapCandidate = Path.Combine(output, Path.GetFileName(mapInput));
SFUtil.EncryptERRegulation(regulationCandidate, regulation, regulation.Compression);
map.Write(mapCandidate);
var baselineRegulation = SFUtil.DecryptERRegulation(input);
var actualRegulation = SFUtil.DecryptERRegulation(regulationCandidate);
if (actualRegulation.Files.Count != baselineRegulation.Files.Count ||
    actualRegulation.Version != baselineRegulation.Version || actualRegulation.Compression != baselineRegulation.Compression ||
    actualRegulation.Format != baselineRegulation.Format || actualRegulation.BigEndian != baselineRegulation.BigEndian ||
    actualRegulation.BitBigEndian != baselineRegulation.BitBigEndian || actualRegulation.Unicode != baselineRegulation.Unicode ||
    actualRegulation.Extended != baselineRegulation.Extended || actualRegulation.Unk04 != baselineRegulation.Unk04 ||
    actualRegulation.Unk05 != baselineRegulation.Unk05) throw new Exception("Regulation binder metadata changed");
for (var i = 0; i < baselineRegulation.Files.Count; i++) {
    var a = baselineRegulation.Files[i]; var b = actualRegulation.Files[i];
    if (a.Name != b.Name || a.ID != b.ID || a.Flags != b.Flags || a.CompressionType != b.CompressionType)
        throw new Exception("Regulation member metadata changed");
    if (Path.GetFileNameWithoutExtension(a.Name) is not ("NpcParam" or "TalkParam") &&
        !a.Bytes.Span.SequenceEqual(b.Bytes.Span))
        throw new Exception("Unrelated parameter table changed");
}
var readback = Read(actualRegulation);
if (Rows(readback) != Rows(table)) throw new Exception("NpcParam readback mismatch");
if (Rows(readback, carrierNpc) != beforeRows) throw new Exception("Existing NpcParam row changed");
var talkReadback = ReadTalk(actualRegulation);
string TalkRows(Param value) => JsonSerializer.Serialize(value.Rows.Select(row => new {
    row.ID, row.Name, Cells = row.Cells.ToDictionary(c => c.Def.InternalName, c => c.Value)
}));
if (TalkRows(talkReadback) != TalkRows(talk)) throw new Exception("TalkParam readback mismatch");
talkReadback.Rows.Single(r => r.ID == 99980001).Name = "Hadeon: Ancient is mine oath.";
if (TalkRows(talkReadback) != TalkRows(ReadTalk(baselineRegulation)))
    throw new Exception("Other TalkParam rows or fields changed");

var mapReadback = MSBE.Read(mapCandidate);
var options = new JsonSerializerOptions { IncludeFields = true };
string MapJson(MSBE value) => JsonSerializer.Serialize(new {
    Map = JsonSerializer.SerializeToElement(value, options),
    Regions = value.Regions.GetEntries().Select(region => new {
        Type = region.GetType().FullName,
        Data = JsonSerializer.Serialize(region, region.GetType(), options),
        Shape = JsonSerializer.Serialize(region.Shape, region.Shape.GetType(), options)
    }).ToArray()
});
if (MapJson(mapReadback) != MapJson(map)) throw new Exception("Map readback mismatch");
var resultPart = mapReadback.Parts.Enemies.Single(p => p.EntityID == carrierEntity);
if (resultPart.Name != newPart.Name || resultPart.NPCParamID != carrierNpc || resultPart.TalkID != 0 ||
    resultPart.Position != hadeon.Position) throw new Exception("Carrier map fields changed");
mapReadback.Parts.Enemies.Remove(resultPart);
if (MapJson(mapReadback) != MapJson(MSBE.Read(mapInput))) throw new Exception("Existing map data changed");
if (Hash(input) != inputHash || Hash(mapInput) != mapInputHash) throw new Exception("Input changed during build");
File.WriteAllText(Path.Combine(output, "validation.json"), JsonSerializer.Serialize(new {
    input, inputHash, regulationCandidate, regulationHash = Hash(regulationCandidate),
    mapInput, mapInputHash, mapCandidate, mapHash = Hash(mapCandidate),
    carrierEntity, carrierNpc, nativeTemplateEntity = 18000852, nativeTemplateNpc = 47210070,
    soundAddBankId = 9998, enableSoundObjDist = 100, updatedTalkParamRow = 99980001,
    preservedOtherTablesAndMetadata = true, preservedExistingNpcParamRows = true,
    preservedExistingMapPartsAndRegions = true, gameplayVerified = false
}, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine("Validated hidden native sound carrier, NpcParam clone and first-entrance TalkParam name; all other decoded map/parameter data preserved.");
