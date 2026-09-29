using SoulsFormats;
using Andre.Formats;
using System.Runtime.Loader;
using System.Text.Json;
using System.Security.Cryptography;

// Builds an isolated candidate; never replaces source or deployed files.
if (args.Length != 3) throw new ArgumentException("regulation.bin output-directory Smithbox-directory");
var input = Path.GetFullPath(args[0]);
var output = Path.GetFullPath(args[1]);
var lib = Path.GetFullPath(args[2]);
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
Directory.CreateDirectory(output);
AssemblyLoadContext.Default.Resolving += (c, n) => {
    var path = Path.Combine(lib, n.Name + ".dll");
    return File.Exists(path) ? c.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(lib);
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();
var inputHash = Hash(input);
var binder = SFUtil.DecryptERRegulation(input);
var defs = Directory.GetFiles(Path.Combine(lib, "Assets/PARAM/ER/Defs"), "*.xml")
    .Select(f => PARAMDEF.XmlDeserialize(f, true)).ToDictionary(d => d.ParamType);
Param Read(BND4 b) {
    var p = Param.Read(b.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "SpEffectParam").Bytes);
    p.ApplyParamdef(defs[p.ParamType], ulong.Parse(b.Version), "SpEffectParam");
    return p;
}
string Row(Param.Row r) => JsonSerializer.Serialize(new {r.ID, r.Name,
    cells = r.Cells.ToDictionary(c => c.Def.InternalName, c => c.Value)});
var param = Read(binder);
var original = param.Rows.ToDictionary(r => r.ID, Row);
var changes = new List<object>();
var expected = new Dictionary<long, float> {{102001, .30f}, {102011, .35f},
    {102013, .35f}, {102015, .35f}, {102060, .66f}};
foreach (var pair in expected) {
    var row = param.Rows.Single(r => r.ID == pair.Key);
    var cell = row.Cells.Single(c => c.Def.InternalName == "guardStaminaMult");
    var before = Convert.ToSingle(cell.Value);
    if (Math.Abs(before - pair.Value) > .000001f) throw new Exception("Unexpected deflect baseline: " + pair.Key);
    var after = before * .75f;
    cell.Value = after;
    changes.Add(new {row = pair.Key, field = "guardStaminaMult", before, after});
    cell.Value = before;
    if (Row(row) != original[row.ID]) throw new Exception("Unrelated field change");
    cell.Value = after;
}
foreach (var row in param.Rows.Where(r => !expected.ContainsKey(r.ID)))
    if (Row(row) != original[row.ID]) throw new Exception("Unrelated row change");
binder.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "SpEffectParam").Bytes = param.Write();
var candidate = Path.Combine(output, "regulation.bin");
SFUtil.EncryptERRegulation(candidate, binder, binder.Compression);
var actual = SFUtil.DecryptERRegulation(candidate);
var baseline = SFUtil.DecryptERRegulation(input);
if (actual.Files.Count != baseline.Files.Count || actual.Version != baseline.Version
    || actual.Compression != baseline.Compression || actual.Format != baseline.Format
    || actual.BigEndian != baseline.BigEndian || actual.BitBigEndian != baseline.BitBigEndian
    || actual.Unicode != baseline.Unicode || actual.Extended != baseline.Extended
    || actual.Unk04 != baseline.Unk04 || actual.Unk05 != baseline.Unk05)
    throw new Exception("Binder metadata changed");
for (var i = 0; i < baseline.Files.Count; i++) {
    var a = baseline.Files[i]; var b = actual.Files[i];
    if (a.Name != b.Name || a.ID != b.ID || a.Flags != b.Flags || a.CompressionType != b.CompressionType)
        throw new Exception("Member metadata changed");
    if (Path.GetFileNameWithoutExtension(a.Name) != "SpEffectParam" && !a.Bytes.Span.SequenceEqual(b.Bytes.Span))
        throw new Exception("Unrelated parameter table changed");
}
if (!Read(actual).Rows.Select(Row).SequenceEqual(param.Rows.Select(Row))) throw new Exception("Readback differs");
if (Hash(input) != inputHash) throw new Exception("Input changed during build");
var receipt = new {input, inputHash, candidate, sha256 = Hash(candidate), changes,
    unrelatedMembersPreserved = true, fullRowReadbackMatches = true, gameplayVerified = false};
File.WriteAllText(Path.Combine(output, "receipt.json"), JsonSerializer.Serialize(receipt, new JsonSerializerOptions {WriteIndented=true}));
Console.WriteLine($"Verified five deflect multipliers; all other fields/members preserved. {output}");
