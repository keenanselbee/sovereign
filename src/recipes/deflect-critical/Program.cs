using SoulsFormats;
using Andre.Formats;
using System.Runtime.Loader;
using System.Text.Json;
using System.Security.Cryptography;

// Isolated, expected-value guarded candidate. Never writes its input or editors.
if (args.Length != 3) throw new ArgumentException("regulation.bin new-output-directory Smithbox-directory");
var input = Path.GetFullPath(args[0]);
var output = Path.GetFullPath(args[1]);
var lib = Path.GetFullPath(args[2]);
if (Directory.Exists(output)) throw new IOException("Use a new output directory");
AssemblyLoadContext.Default.Resolving += (c, n) => {
    var path = Path.Combine(lib, n.Name + ".dll");
    return File.Exists(path) ? c.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(lib);
string Hash(string p) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(p))).ToLowerInvariant();
var inputHash = Hash(input);
var binder = SFUtil.DecryptERRegulation(input);
var def = PARAMDEF.XmlDeserialize(Path.Combine(lib, "Assets/PARAM/ER/Defs/SpEffect.xml"), true);
Param Read(BND4 b) {
    var p = Param.Read(b.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "SpEffectParam").Bytes);
    p.ApplyParamdef(def, ulong.Parse(b.Version), "SpEffectParam");
    return p;
}
string Row(Param.Row r) => JsonSerializer.Serialize(new { r.ID, r.Name, Cells = r.Cells.ToDictionary(c => c.Def.InternalName, c => c.Value) });
object Get(Param.Row r, string name) => r.Cells.Single(c => c.Def.InternalName == name).Value;
void Set(Param.Row r, string name, object value) {
    var cell = r.Cells.Single(c => c.Def.InternalName == name);
    cell.Value = Convert.ChangeType(value, cell.Value.GetType());
}
var param = Read(binder);
var baseline = param.Rows.ToDictionary(r => r.ID, Row);
int[] ids = [1627611, 1627612, 1627613, 1627614];
if (param.Rows.Any(r => ids.Contains(r.ID))) throw new Exception("Critical effect IDs already occupied");
foreach (var member in binder.Files.Where(f => Path.GetFileNameWithoutExtension(f.Name) != "SpEffectParam"))
foreach (var id in ids)
    if (member.Bytes.Span.IndexOf(BitConverter.GetBytes(id)) >= 0) throw new Exception($"ID {id} referenced in {member.Name}");
foreach (var row in param.Rows)
foreach (var cell in row.Cells)
    if (cell.Value is int or uint or long or ulong && ids.Any(id => Convert.ToInt64(cell.Value) == id))
        throw new Exception($"ID referenced by SpEffect {row.ID}/{cell.Def.InternalName}");
foreach (var id in Enumerable.Range(102007, 4)) {
    var row = param.Rows.Single(r => r.ID == id);
    if (Convert.ToSingle(Get(row, "effectEndurance")) != 3f) throw new Exception($"Charge {id} duration drift");
    Set(row, "effectEndurance", 7f);
    var edited = Row(row); Set(row, "effectEndurance", 3f);
    if (Row(row) != baseline[id]) throw new Exception("Unexpected charge-field edit");
    Set(row, "effectEndurance", 7f);
}
var donor = param.Rows.Single(r => r.ID == 320900);
string[] rates = ["physicsAttackRate", "magicAttackRate", "fireAttackRate", "thunderAttackRate", "darkAttackRate"];
if (Convert.ToInt32(Get(donor, "throwAttackParamChange")) != 1 || Convert.ToInt32(Get(donor, "stateInfo")) != 367
    || rates.Any(k => Math.Abs(Convert.ToSingle(Get(donor, k)) - 1.17f) > .000001f))
    throw new Exception("Dagger Talisman native critical effect changed");
for (int tier = 1; tier <= 4; tier++) {
    var row = new Param.Row(donor) { ID = ids[tier - 1], Name = $"Sovereign - Deflect critical {tier} charge(s)" };
    foreach (var key in rates) Set(row, key, 1f + tier * .1f);
    Set(row, "effectEndurance", -1f);
    Set(row, "iconId", -1);
    // Independent conditional bonus; it must coexist with the equipped talisman.
    Set(row, "spCategory", 0);
    Set(row, "categoryPriority", 0);
    param.AddRow(row);
}
foreach (var row in param.Rows.Where(r => !ids.Contains(r.ID) && (r.ID < 102007 || r.ID > 102010)))
    if (Row(row) != baseline[row.ID]) throw new Exception($"Unrelated row changed: {row.ID}");
binder.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "SpEffectParam").Bytes = param.Write();
Directory.CreateDirectory(output);
var candidate = Path.Combine(output, "regulation.bin");
SFUtil.EncryptERRegulation(candidate, binder, binder.Compression);
var actual = SFUtil.DecryptERRegulation(candidate);
var original = SFUtil.DecryptERRegulation(input);
if (actual.Files.Count != original.Files.Count || actual.Version != original.Version || actual.Compression != original.Compression
    || actual.Format != original.Format || actual.BigEndian != original.BigEndian || actual.BitBigEndian != original.BitBigEndian
    || actual.Unicode != original.Unicode || actual.Extended != original.Extended || actual.Unk04 != original.Unk04 || actual.Unk05 != original.Unk05)
    throw new Exception("Binder metadata changed");
for (int i = 0; i < actual.Files.Count; i++) {
    var a = original.Files[i]; var b = actual.Files[i];
    if (a.ID != b.ID || a.Name != b.Name || a.Flags != b.Flags || a.CompressionType != b.CompressionType)
        throw new Exception("Member metadata changed");
    if (Path.GetFileNameWithoutExtension(a.Name) != "SpEffectParam" && !a.Bytes.Span.SequenceEqual(b.Bytes.Span))
        throw new Exception("Unrelated table changed");
}
if (!Read(actual).Rows.Select(Row).SequenceEqual(param.Rows.Select(Row))) throw new Exception("Full readback mismatch");
if (Hash(input) != inputHash) throw new Exception("Input drift");
File.WriteAllText(Path.Combine(output, "validation.json"), JsonSerializer.Serialize(new {
    input, inputHash, candidate, outputHash = Hash(candidate), durationRows = Enumerable.Range(102007, 4), duration = 7,
    criticalRows = ids, nativeTemplate = 320900, criticalRates = new[] {1.1, 1.2, 1.3, 1.4},
    donor = JsonSerializer.Deserialize<JsonElement>(Row(donor)),
    completeReadbackMatches = true, otherRowsTablesAndMetadataPreserved = true, gameplayVerified = false
}, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine($"Verified four duration edits and four critical-only effect additions: {candidate}");
