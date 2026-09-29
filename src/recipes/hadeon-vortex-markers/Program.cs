using Andre.Formats;
using SoulsFormats;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text.Json;

// Isolated candidate builder: create the marker rows or repair their duration.
var repairDuration = args.Length == 5 && args[0] == "--repair-duration";
if (!repairDuration && args.Length != 4) throw new ArgumentException(
    "[--repair-duration] regulation.bin candidate-directory Smithbox-tools retained-vanilla-event-directory");
var argumentOffset = repairDuration ? 1 : 0;
var input = Path.GetFullPath(args[argumentOffset]);
var output = Path.GetFullPath(args[argumentOffset + 1]);
var library = Path.GetFullPath(args[argumentOffset + 2]);
var vanillaEvents = Path.GetFullPath(args[argumentOffset + 3]);
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
if (!File.Exists(input) || (!repairDuration && !Directory.Exists(vanillaEvents)))
    throw new FileNotFoundException("A regulation or retained vanilla event input is missing");
AssemblyLoadContext.Default.Resolving += (context, name) => {
    var path = Path.Combine(library, name.Name + ".dll");
    return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(library);
const int templateId = 5039;
int[] markerIds = [1627600, 1627601];
var inputHash = Hash(input);
var binder = SFUtil.DecryptERRegulation(input);
var definition = PARAMDEF.XmlDeserialize(Path.Combine(library, "Assets/PARAM/ER/Defs/SpEffect.xml"), true);
Param Read(BND4 value) {
    var param = Param.Read(value.Files.Single(file => Path.GetFileNameWithoutExtension(file.Name) == "SpEffectParam").Bytes);
    param.ApplyParamdef(definition, ulong.Parse(value.Version), "SpEffectParam");
    return param;
}
string Rows(Param value, int[]? omit = null) => JsonSerializer.Serialize(value.Rows
    .Where(row => omit == null || !omit.Contains(row.ID)).Select(row => new {
    row.ID, row.Name, Cells = row.Cells.ToDictionary(cell => cell.Def.InternalName, cell => cell.Value)
}));
string Cells(Param.Row row) => JsonSerializer.Serialize(row.Cells.ToDictionary(cell => cell.Def.InternalName, cell => cell.Value));
var effects = Read(binder);
var template = effects.Rows.Single(row => row.ID == templateId);
int Field(string name) => Convert.ToInt32(template.Cells.Single(cell => cell.Def.InternalName == name).Value);
if (Field("iconId") != -1 || Field("behaviorId") != -1 || Field("spCategory") != 0 ||
    Field("replaceSpEffectId") != -1 || Field("cycleOccurrenceSpEffectId") != -1 ||
    Field("atkOccurrenceSpEffectId") != -1 || Field("effectEndurance") != 0)
    throw new Exception("Native neutral template 5039 changed; review marker behavior");
var beforeWithoutMarkers = Rows(effects, markerIds);
var templateCells = Cells(template);
var expectedMarker = new Param.Row(template);
expectedMarker.Cells.Single(cell => cell.Def.InternalName == "effectEndurance").Value = 0.1f;
var expectedMarkerCells = Cells(expectedMarker);
var names = new[] { "Sovereign - Hadeon vortex live marker", "Sovereign - Hadeon vortex cue marker" };
var scannedEventFiles = 0;

if (repairDuration) {
    for (var index = 0; index < markerIds.Length; index++) {
        var marker = effects.Rows.Single(row => row.ID == markerIds[index]);
        if (marker.Name != names[index] || Cells(marker) != templateCells)
            throw new Exception($"Marker {markerIds[index]} differs from the original neutral template");
        marker.Cells.Single(cell => cell.Def.InternalName == "effectEndurance").Value = 0.1f;
    }
} else {
    if (markerIds.Any(id => effects.Rows.Any(row => row.ID == id)))
        throw new Exception("One of the marker SpEffect IDs is already occupied");
    // Detect old references in all regulation members and compiled mod/retained vanilla events.
    foreach (var member in binder.Files)
    foreach (var id in markerIds)
        if (Path.GetFileNameWithoutExtension(member.Name) != "SpEffectParam" &&
            member.Bytes.Span.IndexOf(BitConverter.GetBytes(id)) is var offset && offset >= 0)
            throw new Exception($"Marker ID {id} occurs in regulation member {member.Name} at byte {offset}");
    foreach (var row in effects.Rows)
    foreach (var cell in row.Cells)
        if (cell.Value is int or uint or long or ulong &&
            markerIds.Any(id => Convert.ToInt64(cell.Value) == id))
            throw new Exception($"Marker ID occurs in SpEffectParam row {row.ID}, field {cell.Def.InternalName}");
    var modEvents = Path.Combine(Directory.GetParent(input)!.FullName, "event");
    if (!Directory.Exists(modEvents)) throw new DirectoryNotFoundException(modEvents);
    var eventFiles = Directory.GetFiles(modEvents, "*.emevd.dcx")
        .Concat(Directory.GetFiles(vanillaEvents, "*.emevd.dcx")).ToArray();
    scannedEventFiles = eventFiles.Length;
    foreach (var path in eventFiles)
    foreach (var instruction in EMEVD.Read(path).Events.SelectMany(e => e.Instructions))
    foreach (var id in markerIds)
        if (instruction.ArgData.AsSpan().IndexOf(BitConverter.GetBytes(id)) >= 0)
            throw new Exception($"Marker ID {id} occurs in event {path}");

    for (var index = 0; index < markerIds.Length; index++) {
        var marker = new Param.Row(template) { ID = markerIds[index], Name = names[index] };
        if (Cells(marker) != templateCells) throw new Exception("Marker cells differ from native template");
        marker.Cells.Single(cell => cell.Def.InternalName == "effectEndurance").Value = 0.1f;
        effects.AddRow(marker);
    }
}
var expected = Rows(effects);
binder.Files.Single(file => Path.GetFileNameWithoutExtension(file.Name) == "SpEffectParam").Bytes = effects.Write();
Directory.CreateDirectory(output);
var candidate = Path.Combine(output, "regulation.bin");
SFUtil.EncryptERRegulation(candidate, binder, binder.Compression);
var baseline = SFUtil.DecryptERRegulation(input);
var actual = SFUtil.DecryptERRegulation(candidate);
if (actual.Files.Count != baseline.Files.Count || actual.Version != baseline.Version ||
    actual.Compression != baseline.Compression || actual.Format != baseline.Format ||
    actual.BigEndian != baseline.BigEndian || actual.BitBigEndian != baseline.BitBigEndian ||
    actual.Unicode != baseline.Unicode || actual.Extended != baseline.Extended ||
    actual.Unk04 != baseline.Unk04 || actual.Unk05 != baseline.Unk05)
    throw new Exception("Binder metadata drift");
for (var index = 0; index < baseline.Files.Count; index++) {
    var a = baseline.Files[index];
    var b = actual.Files[index];
    if (a.Name != b.Name || a.ID != b.ID || a.Flags != b.Flags || a.CompressionType != b.CompressionType)
        throw new Exception("Binder member metadata drift");
    if (Path.GetFileNameWithoutExtension(a.Name) != "SpEffectParam" && !a.Bytes.Span.SequenceEqual(b.Bytes.Span))
        throw new Exception($"Unrelated parameter member changed: {a.Name}");
}
var readback = Read(actual);
if (Rows(readback) != expected) throw new Exception("SpEffect native readback differs from expected table");
foreach (var id in markerIds) {
    var row = readback.Rows.Single(value => value.ID == id);
    if (Cells(row) != expectedMarkerCells)
        throw new Exception($"Marker {id} differs from 5039 beyond ID/name and duration");
}
if (Rows(readback, markerIds) != beforeWithoutMarkers) throw new Exception("Unrelated SpEffect rows changed");
if (Hash(input) != inputHash) throw new Exception("Input changed during candidate build");
File.WriteAllText(Path.Combine(output, "validation.json"), JsonSerializer.Serialize(new {
    input, inputSha256 = inputHash, candidate, candidateSha256 = Hash(candidate),
    mode = repairDuration ? "repair-duration" : "create", templateId, markerIds, names,
    effectEnduranceBefore = repairDuration ? 0f : (float?)null, effectEnduranceAfter = 0.1f,
    scannedEventFiles,
    scannedRegulationMembers = baseline.Files.Count, decodedReadback = true,
    allUnrelatedSpEffectRowsPreserved = true, allOtherTablesAndBinderMetadataPreserved = true,
    onlyIdNameAndDurationDifferFromTemplate = true, gameplayVerified = false
}, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine($"Validated two 0.1-second marker rows and {baseline.Files.Count} regulation members; unrelated decoded content preserved.");

static string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();
