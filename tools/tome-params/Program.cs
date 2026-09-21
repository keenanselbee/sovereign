// Guarded native parameter candidate builder. Never writes the source or an editor/live path.
using SoulsFormats;
using Andre.Formats;
using System.Runtime.Loader;
using System.Text.Json;
using System.Security.Cryptography;

var source = Path.GetFullPath(args[0]);
var planPath = Path.GetFullPath(args[1]);
var output = Path.GetFullPath(args[2]);
var lib = Path.GetFullPath(args[3]);
if (source == output || File.Exists(output)) throw new Exception("Output must be a new candidate");
AssemblyLoadContext.Default.Resolving += (c, n) => {
    var path = Path.Combine(lib, n.Name + ".dll");
    return File.Exists(path) ? c.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(lib);
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)));
var sourceHash = Hash(source);
var plan = JsonDocument.Parse(File.ReadAllText(planPath)).RootElement;
if (!sourceHash.Equals(plan.GetProperty("sourceHash").GetString(), StringComparison.OrdinalIgnoreCase))
    throw new Exception("Regulation baseline changed");
var binder = SFUtil.DecryptERRegulation(source);
var defs = Directory.GetFiles(Path.Combine(lib, "Assets/PARAM/ER/Defs"), "*.xml")
    .Select(p => PARAMDEF.XmlDeserialize(p, true)).ToDictionary(d => d.ParamType);
Param Parse(BinderFile file, string name) {
    var p = Param.Read(file.Bytes);
    p.ApplyParamdef(defs[p.ParamType], ulong.Parse(binder.Version), name);
    return p;
}
var changes = plan.GetProperty("changes").EnumerateArray().ToArray();
if (changes.Select(c => (c.GetProperty("table").GetString(), c.GetProperty("id").GetInt32())).Distinct().Count() != changes.Length)
    throw new Exception("Duplicate row patch");
var report = new List<object>();
foreach (var group in changes.GroupBy(c => c.GetProperty("table").GetString())) {
    var file = binder.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == group.Key);
    var baseline = Parse(file, group.Key);
    var target = Parse(file, group.Key);
    if (!target.Write().AsSpan().SequenceEqual(file.Bytes.Span))
        throw new Exception("Unchanged table does not roundtrip byte-exactly: " + group.Key);
    foreach (var change in group) {
        int id = change.GetProperty("id").GetInt32();
        var clone = change.GetProperty("clone");
        Param.Row row;
        if (clone.ValueKind != JsonValueKind.Null) {
            if (target.Rows.Any(r => r.ID == id)) throw new Exception("Allocated row already exists");
            row = new Param.Row(baseline[clone.GetInt32()], target) { ID = id };
            target.InsertRow(target.Rows.TakeWhile(r => r.ID < id).Count(), row);
        } else {
            row = target[id] ?? throw new Exception("Missing original row");
        }
        foreach (var edit in change.GetProperty("after").EnumerateObject()) {
            var cell = row.Cells.Single(c => c.Def.InternalName == edit.Name);
            var before = change.GetProperty("before").GetProperty(edit.Name);
            if (JsonSerializer.Serialize(cell.Value) != before.GetRawText())
                throw new Exception($"Unexpected field baseline {group.Key}:{id}:{edit.Name}");
            cell.Value = JsonSerializer.Deserialize(edit.Value.GetRawText(), cell.Value.GetType());
        }
        if (change.GetProperty("name").ValueKind != JsonValueKind.Null)
            row.Name = change.GetProperty("name").GetString();
    }
    file.Bytes = target.Write();
    var reread = Parse(file, group.Key);
    if (!target.Rows.Select(r => r.ID).SequenceEqual(reread.Rows.Select(r => r.ID)))
        throw new Exception("Row ordering changed on serialization");
    foreach (var row in target.Rows)
        if (row.Name != reread[row.ID].Name || !row.DataEquals(reread[row.ID]))
            throw new Exception("Decoded candidate differs from exact expected rows");
    foreach (var row in baseline.Rows.Where(r => !group.Any(c => c.GetProperty("id").GetInt32() == r.ID)))
        if (row.Name != reread[row.ID].Name || !row.DataEquals(reread[row.ID]))
            throw new Exception("Unreviewed original row changed");
    report.Add(new { table = group.Key, originalRows = baseline.Rows.Count, finalRows = reread.Rows.Count,
        changedRows = group.Select(c => c.GetProperty("id").GetInt32()).ToArray(), unchangedRoundtripByteExact = true });
}
if (Hash(source) != sourceHash) throw new Exception("Source drift before write");
SFUtil.EncryptERRegulation(output, binder, binder.Compression);
var saved = SFUtil.DecryptERRegulation(output);
if (saved.Version != binder.Version || saved.Files.Count != binder.Files.Count)
    throw new Exception("Binder identity changed");
for (int i = 0; i < binder.Files.Count; i++) {
    var a = binder.Files[i]; var b = saved.Files[i];
    if (a.ID != b.ID || a.Name != b.Name || a.Flags != b.Flags || a.CompressionType != b.CompressionType
        || !a.Bytes.Span.SequenceEqual(b.Bytes.Span)) throw new Exception("Binder preservation mismatch");
}
if (Hash(source) != sourceHash) throw new Exception("Source drift after write");
var receipt = new { source, sourceHash, output, outputHash = Hash(output), tables = report,
    planHash = Hash(planPath), gameplayVerified = false };
File.WriteAllText(output + ".receipt.json", JsonSerializer.Serialize(receipt, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine(JsonSerializer.Serialize(receipt));
