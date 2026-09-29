using SoulsFormats;
using Andre.Formats;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text.Json;

// Guarded candidate builder; inputs and editor workspaces are never overwritten.
if (args.Length != 5) throw new ArgumentException("regulation.bin output-directory Smithbox-directory logic-id map.msb.dcx");
var input = Path.GetFullPath(args[0]);
var output = Path.GetFullPath(args[1]);
var lib = Path.GetFullPath(args[2]);
var logicId = int.Parse(args[3]);
var mapInput = Path.GetFullPath(args[4]);
const int privateThinkId = 25009900;
if (logicId != 250090) throw new ArgumentException("Expected the private Hadeon logic ID 250090");
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
AssemblyLoadContext.Default.Resolving += (context, name) => {
    var path = Path.Combine(lib, name.Name + ".dll");
    return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(lib);
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)));
var inputHash = Hash(input);
var mapInputHash = Hash(mapInput);
var original = SFUtil.DecryptERRegulation(input);
var def = PARAMDEF.XmlDeserialize(Path.Combine(lib, "Assets/PARAM/ER/Defs/NpcThinkParam.xml"), true);
Param Read(BND4 binder) {
    var value = Param.Read(binder.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "NpcThinkParam").Bytes);
    value.ApplyParamdef(def, ulong.Parse(binder.Version), "NpcThinkParam");
    return value;
}
string Rows(Param value, int? omit = null) => JsonSerializer.Serialize(value.Rows.Where(row => row.ID != omit).Select(row => new {
    row.ID, row.Name, Cells = row.Cells.ToDictionary(c => c.Def.InternalName, c => c.Value)
}));
var npc = Read(original);
var before = Rows(npc);
if (npc.Rows.Any(r => Convert.ToInt32(r.Cells.Single(c => c.Def.InternalName == "logicId").Value) == logicId))
    throw new Exception("Private logic ID is already assigned; review before replacing it");
if (npc.Rows.Any(r => r.ID == privateThinkId)) throw new Exception("Private Think ID is occupied");
var template = npc.Rows.Single(r => r.ID == 25009000);
var row = new Param.Row(template) { ID = privateThinkId, Name = "Sovereign - Hadeon speech AI" };
var cell = row.Cells.Single(c => c.Def.InternalName == "logicId");
if (Convert.ToInt32(cell.Value) != 10000) throw new Exception("Expected Hadeon's native common logic 10000; review baseline");
if (Convert.ToInt32(row.Cells.Single(c => c.Def.InternalName == "battleGoalID").Value) != 250010)
    throw new Exception("Expected unchanged native Crucible Knight battle goal 250010");
var oldValue = cell.Value;
cell.Value = Convert.ChangeType(logicId, oldValue.GetType());
npc.AddRow(row);
var expected = Rows(npc);
original.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "NpcThinkParam").Bytes = npc.Write();
Directory.CreateDirectory(output);
var candidate = Path.Combine(output, "regulation.bin");
SFUtil.EncryptERRegulation(candidate, original, original.Compression);
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
    if (Path.GetFileNameWithoutExtension(a.Name) != "NpcThinkParam" && !a.Bytes.Span.SequenceEqual(b.Bytes.Span))
        throw new Exception("Unrelated table changed");
}
var readback = Read(actual);
if (Rows(readback) != expected) throw new Exception("Readback differs from expected Think table");
if (Rows(readback, privateThinkId) != before) throw new Exception("An original Think row or field changed");
// Change only Hadeon's map assignment; preserve all region geometry and other actors.
var map = MSBE.Read(mapInput);
var jsonOptions = new JsonSerializerOptions { IncludeFields = true };
string Json(object value) => JsonSerializer.Serialize(value, value.GetType(), jsonOptions);
object MapState(MSBE value) => new {
    Map = JsonSerializer.SerializeToElement(value, jsonOptions),
    Regions = value.Regions.GetEntries().Select(region => new {
        Type = region.GetType().FullName, Data = Json(region), Shape = Json(region.Shape)
    }).ToArray()
};
var mapBefore = Json(MapState(map));
var actor = map.Parts.Enemies.Single(p => p.EntityID == 18002354);
if (actor.ThinkParamID != 25009000) throw new Exception("Hadeon map Think assignment changed");
actor.ThinkParamID = privateThinkId;
var mapCandidate = Path.Combine(output, Path.GetFileName(mapInput));
map.Write(mapCandidate);
var mapReadback = MSBE.Read(mapCandidate);
if (Json(MapState(mapReadback)) != Json(MapState(map))) throw new Exception("Map readback mismatch");
mapReadback.Parts.Enemies.Single(p => p.EntityID == 18002354).ThinkParamID = 25009000;
if (Json(MapState(mapReadback)) != mapBefore) throw new Exception("Unrelated map data changed");
if (Hash(input) != inputHash || Hash(mapInput) != mapInputHash) throw new Exception("Input changed during build");
File.WriteAllText(Path.Combine(output, "validation.json"), JsonSerializer.Serialize(new {
    input, inputHash, candidate, outputHash = Hash(candidate), template = 25009000, addedRow = privateThinkId,
    field = "logicId", before = 10000, after = logicId,
    mapInput, mapInputHash, mapCandidate, mapOutputHash = Hash(mapCandidate),
    actor = 18002354, thinkBefore = 25009000, thinkAfter = privateThinkId,
    preservedOtherTablesAndMetadata = true, preservedAllOriginalThinkRows = true,
    preservedAllOtherMapData = true, gameplayVerified = false
}, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine("Verified private Think clone and one map assignment; all original Think rows, unrelated tables and other decoded map data preserved.");
