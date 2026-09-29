using SoulsFormats;
using Andre.Formats;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text.Json;

// Isolated candidate builder. It never overwrites its input or an editor file.
if (args.Length != 3) throw new ArgumentException("regulation.bin output-directory Smithbox-directory");
var input = Path.GetFullPath(args[0]);
var output = Path.GetFullPath(args[1]);
var lib = Path.GetFullPath(args[2]);
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
AssemblyLoadContext.Default.Resolving += (context, name) => {
    var path = Path.Combine(lib, name.Name + ".dll");
    return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(lib);
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)));
var inputHash = Hash(input);
var binder = SFUtil.DecryptERRegulation(input);
var def = PARAMDEF.XmlDeserialize(Path.Combine(lib, "Assets/PARAM/ER/Defs/SpEffect.xml"), true);
Param Read(BND4 value) {
    var param = Param.Read(value.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "SpEffectParam").Bytes);
    param.ApplyParamdef(def, ulong.Parse(value.Version), "SpEffectParam");
    return param;
}
string Rows(Param value, int? omitFirst = null, int? omitLast = null) => JsonSerializer.Serialize(value.Rows
    .Where(row => !omitFirst.HasValue || row.ID < omitFirst || row.ID > omitLast)
    .Select(row => new { row.ID, row.Name, Cells = row.Cells.ToDictionary(c => c.Def.InternalName, c => c.Value) }));
var effects = Read(binder);
if (effects.Rows.Any(row => row.ID >= 1627161 && row.ID <= 1627170))
    throw new Exception("Cooldown row range 1627161-1627170 is occupied");
var existing = effects.Rows.Single(row => row.ID == 1627127);
var duration = existing.Cells.Single(cell => cell.Def.InternalName == "effectEndurance");
if (Math.Abs(Convert.ToSingle(duration.Value) - 30f) > 0.00001f)
    throw new Exception("Expected the existing 30-second outside-arena cooldown");
var before = Rows(effects);
duration.Value = Convert.ChangeType(40f, duration.Value.GetType());
for (int deaths = 1; deaths <= 10; deaths++) {
    var row = new Param.Row(existing) {
        ID = 1627160 + deaths,
        Name = $"Sovereign - Hadeon rescue cooldown after {deaths} losses"
    };
    row.Cells.Single(cell => cell.Def.InternalName == "effectEndurance").Value =
        Convert.ChangeType(40f - 2f * deaths, duration.Value.GetType());
    effects.AddRow(row);
}
var expected = Rows(effects);
binder.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "SpEffectParam").Bytes = effects.Write();
Directory.CreateDirectory(output);
var candidate = Path.Combine(output, "regulation.bin");
SFUtil.EncryptERRegulation(candidate, binder, binder.Compression);
var actual = SFUtil.DecryptERRegulation(candidate);
var baseline = SFUtil.DecryptERRegulation(input);
if (actual.Files.Count != baseline.Files.Count || actual.Version != baseline.Version || actual.Compression != baseline.Compression
    || actual.Format != baseline.Format || actual.BigEndian != baseline.BigEndian || actual.BitBigEndian != baseline.BitBigEndian
    || actual.Unicode != baseline.Unicode || actual.Extended != baseline.Extended || actual.Unk04 != baseline.Unk04 || actual.Unk05 != baseline.Unk05)
    throw new Exception("Binder metadata drift");
for (int i = 0; i < baseline.Files.Count; i++) {
    var a = baseline.Files[i]; var b = actual.Files[i];
    if (a.Name != b.Name || a.ID != b.ID || a.Flags != b.Flags || a.CompressionType != b.CompressionType)
        throw new Exception("Member metadata drift");
    if (Path.GetFileNameWithoutExtension(a.Name) != "SpEffectParam" && !a.Bytes.Span.SequenceEqual(b.Bytes.Span))
        throw new Exception("Unrelated table changed");
}
var readback = Read(actual);
if (Rows(readback) != expected) throw new Exception("SpEffect readback mismatch");
readback.Rows.Single(row => row.ID == 1627127).Cells.Single(cell => cell.Def.InternalName == "effectEndurance").Value = 30f;
if (Rows(readback, 1627161, 1627170) != before)
    throw new Exception("An unrelated original SpEffect row or field changed");
if (Hash(input) != inputHash) throw new Exception("Input changed during candidate build");
File.WriteAllText(Path.Combine(output, "validation.json"), JsonSerializer.Serialize(new {
    input, inputHash, candidate, outputHash = Hash(candidate), template = 1627127,
    changedDuration = new { before = 30, after = 40 }, addedRange = new[] { 1627161, 1627170 },
    addedDurations = Enumerable.Range(1, 10).Select(deaths => 40 - 2 * deaths).ToArray(),
    preservedOtherTablesAndMetadata = true, preservedAllOtherOriginalSpEffects = true,
    gameplayVerified = false
}, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine("Verified 40-second default and ten descending cooldown rows; unrelated rows and tables preserved.");
