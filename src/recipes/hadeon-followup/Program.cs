using SoulsFormats;
using Andre.Formats;
using System.Runtime.Loader;
using System.Text.Json;
using System.Numerics;
using System.Security.Cryptography;

// An isolated, guarded candidate builder. Never writes input files or editor workspaces.
if (args.Length != 4) throw new ArgumentException("regulation.bin map.msb.dcx output-directory Smithbox-directory");
var inputReg = Path.GetFullPath(args[0]);
var inputMap = Path.GetFullPath(args[1]);
var output = Path.GetFullPath(args[2]);
var lib = Path.GetFullPath(args[3]);
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
Directory.CreateDirectory(output);
AssemblyLoadContext.Default.Resolving += (context, name) => {
    var path = Path.Combine(lib, name.Name + ".dll");
    return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(lib);
var jsonOptions = new JsonSerializerOptions { IncludeFields = true };
string Json(object value) => JsonSerializer.Serialize(value, value.GetType(), jsonOptions);
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();
var original = SFUtil.DecryptERRegulation(inputReg);
var defs = Directory.GetFiles(Path.Combine(lib, "Assets/PARAM/ER/Defs"), "*.xml")
    .Select(file => PARAMDEF.XmlDeserialize(file, true)).ToDictionary(def => def.ParamType);
Param Read(BND4 binder) {
    var param = Param.Read(binder.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "SpEffectParam").Bytes);
    param.ApplyParamdef(defs[param.ParamType], ulong.Parse(binder.Version), "SpEffectParam");
    return param;
}
string Row(Param.Row row) => Json(new { row.ID, row.Name, Cells = row.Cells.ToDictionary(c => c.Def.InternalName, c => c.Value) });
var effects = Read(original);
var beforeRows = effects.Rows.ToDictionary(row => row.ID, Row);
var changes = new List<object>();
foreach (var row in effects.Rows.Where(row => row.ID >= 1627141 && row.ID <= 1627160)) {
    var stage = (int)(row.ID - 1627140);
    float before = 1 + stage * 0.025f, after = 1 + stage * 0.05f;
    var cells = row.Cells.Where(c => new[] { "maxHpRate", "maxMpRate", "maxStaminaRate", "guardStaminaMult" }.Contains(c.Def.InternalName)
        || c.Def.InternalName.StartsWith("atkEnemyDmgCorrectRate_") || c.Def.InternalName.StartsWith("atkPlayerDmgCorrectRate_")).ToArray();
    if (cells.Length != 14) throw new Exception("Unexpected aid field inventory");
    foreach (var cell in cells) {
        var oldValue = cell.Def.InternalName == "guardStaminaMult" ? 1 / before : before;
        var newValue = cell.Def.InternalName == "guardStaminaMult" ? 1 / after : after;
        if (Math.Abs(Convert.ToSingle(cell.Value) - oldValue) > 0.000001f) throw new Exception($"Unexpected original value {row.ID}/{cell.Def.InternalName}");
        changes.Add(new { row = row.ID, field = cell.Def.InternalName, before = cell.Value, after = newValue });
        cell.Value = newValue;
    }
}
if (changes.Count != 280) throw new Exception("Expected twenty aid tiers");
// Reverse just the approved cell edits in memory and prove every other row/field survived.
var expectedRows = effects.Rows.ToDictionary(row => row.ID, Row);
var sourceParam = Read(SFUtil.DecryptERRegulation(inputReg));
foreach (var row in effects.Rows) {
    if (row.ID < 1627141 || row.ID > 1627160) {
        if (Row(row) != beforeRows[row.ID]) throw new Exception("Unrelated row change");
    } else {
        var old = sourceParam.Rows.Single(r => r.ID == row.ID);
        foreach (var cell in row.Cells.Where(c => new[] { "maxHpRate", "maxMpRate", "maxStaminaRate", "guardStaminaMult" }.Contains(c.Def.InternalName)
            || c.Def.InternalName.StartsWith("atkEnemyDmgCorrectRate_") || c.Def.InternalName.StartsWith("atkPlayerDmgCorrectRate_")))
            old.Cells.Single(c => c.Def.InternalName == cell.Def.InternalName).Value = cell.Value;
        if (Row(row) != Row(old)) throw new Exception("Unrelated field change");
    }
}
original.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "SpEffectParam").Bytes = effects.Write();
var regOut = Path.Combine(output, "regulation.bin");
SFUtil.EncryptERRegulation(regOut, original, original.Compression);
var actual = SFUtil.DecryptERRegulation(regOut);
var baseline = SFUtil.DecryptERRegulation(inputReg);
if (actual.Files.Count != baseline.Files.Count || actual.Version != baseline.Version || actual.Compression != baseline.Compression
    || actual.Format != baseline.Format || actual.BigEndian != baseline.BigEndian || actual.BitBigEndian != baseline.BitBigEndian
    || actual.Unicode != baseline.Unicode || actual.Extended != baseline.Extended || actual.Unk04 != baseline.Unk04 || actual.Unk05 != baseline.Unk05)
    throw new Exception("Binder header drift");
for (int i = 0; i < baseline.Files.Count; i++) {
    var a = baseline.Files[i]; var b = actual.Files[i];
    if (a.Name != b.Name || a.ID != b.ID || a.Flags != b.Flags || a.CompressionType != b.CompressionType) throw new Exception("Member metadata drift");
    if (Path.GetFileNameWithoutExtension(a.Name) != "SpEffectParam" && !a.Bytes.Span.SequenceEqual(b.Bytes.Span)) throw new Exception("Other parameter table changed");
}
if (!Read(actual).Rows.Select(Row).SequenceEqual(effects.Rows.Select(Row))) throw new Exception("Parameter readback mismatch");

var map = MSBE.Read(inputMap);
object MapState(MSBE value) => new { Map = JsonSerializer.SerializeToElement(value, jsonOptions),
    Regions = value.Regions.GetEntries().Select(r => new { Type = r.GetType().Name, Data = Json(r), Shape = Json(r.Shape) }) };
var mapBefore = Json(MapState(map));
var mapRoundtrip = Path.Combine(output, "unchanged-map.msb.dcx");
map.Write(mapRoundtrip);
if (Json(MapState(MSBE.Read(mapRoundtrip))) != mapBefore) throw new Exception("Unchanged map roundtrip failed");
const uint sourceId = 18002366, destinationId = 18002380;
if (map.Parts.GetEntries().Any(p => p.EntityID == destinationId) || map.Regions.GetEntries().Any(r => r.EntityID == destinationId))
    throw new Exception("Return region already present; do not apply twice");
var source = map.Regions.Others.Single(r => r.EntityID == sourceId);
if (Vector3.Distance(source.Position, new Vector3(52.249317f, -75.94449f, 156.27556f)) > 0.001f || Math.Abs(source.Rotation.Y - 64) > 0.001f)
    throw new Exception("Starting point changed; inspect its transform");
var returning = (MSBE.Region.Other)source.DeepCopy();
returning.EntityID = destinationId;
returning.Name = "Sovereign_Hadeon_Return_Barrier";
returning.Rotation = new Vector3(source.Rotation.X, source.Rotation.Y + 180, source.Rotation.Z);
map.Regions.Others.Add(returning);
var mapOut = Path.Combine(output, "m18_00_00_00.msb.dcx");
map.Write(mapOut);
var readback = MSBE.Read(mapOut);
if (Json(MapState(readback)) != Json(MapState(map))) throw new Exception("Edited map roundtrip failed");
readback.Regions.Others.RemoveAll(r => r.EntityID == destinationId);
if (Json(MapState(readback)) != mapBefore) throw new Exception("Unrelated map change");
File.WriteAllText(Path.Combine(output, "validation.json"), Json(new {
    regulation = new { input = inputReg, beforeHash = Hash(inputReg), output = regOut, afterHash = Hash(regOut), changedFields = changes },
    map = new { input = inputMap, beforeHash = Hash(inputMap), output = mapOut, afterHash = Hash(mapOut), sourceId, destinationId,
        returning.Position, returning.Rotation },
    parameterReadback = true, preservedOtherTablesAndMetadata = true, mapRoundtrip = true, onlyOneRegionAdded = true,
    gameplayVerified = false
}));
Console.WriteLine("Validated 280 aid cells (20 tiers), one reversed return region; other decoded content preserved.");
