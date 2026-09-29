using SoulsFormats;
using System.Buffers.Binary;
using System.Numerics;
using System.Security.Cryptography;
using System.Text.Json;
using System.Text.RegularExpressions;

// Offline builder: only the new candidate directory is written. Authored landing
// markers remain authoritative; this recipe regenerates its own helper geometry.
if (args.Length < 5) throw new ArgumentException(
    "map.msb.dcx new-output-directory Smithbox-directory destinations.json event-source.js [--editor-map saved-map.msb.dcx] [event-binary ...]");
var input = Path.GetFullPath(args[0]);
var output = Path.GetFullPath(args[1]);
var library = Path.GetFullPath(args[2]);
var configPath = Path.GetFullPath(args[3]);
var eventSource = Path.GetFullPath(args[4]);
var editorIndex = Array.IndexOf(args, "--editor-map");
if (editorIndex >= 0 && (editorIndex != 5 || args.Length < 7))
    throw new ArgumentException("--editor-map must precede event binaries and name a saved map");
var editorInput = editorIndex >= 0 ? Path.GetFullPath(args[6]) : null;
var binaries = args.Skip(editorIndex >= 0 ? 7 : 5).Select(Path.GetFullPath).ToArray();
var inputs = new[] { input, configPath, eventSource }.Concat(binaries)
    .Concat(editorInput == null ? [] : new[] { editorInput }).Distinct().ToDictionary(path => path, Hash);
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
Directory.SetCurrentDirectory(library);
var config = JsonSerializer.Deserialize<Configuration>(File.ReadAllText(configPath),
    new JsonSerializerOptions { PropertyNameCaseInsensitive = true })!;
var ids = config.Destinations.Select(d => d.EntityId).ToArray();
var pairs = config.PairRegions;
var clearanceByDestination = config.Destinations.ToDictionary(d => d.EntityId, d => d.ClearanceId);
var eligibilityByDestination = config.Destinations.ToDictionary(d => d.EntityId, d => d.EligibilityId);
var helperIds = pairs.Select(p => p.RegionId).Concat(clearanceByDestination.Values)
    .Concat(eligibilityByDestination.Values).ToHashSet();
if (config.SchemaVersion != 1 || ids.Length < 2 || !ids.SequenceEqual(ids.Order()) ||
    ids.Distinct().Count() != ids.Length || ids.Contains(18002390u) || helperIds.Contains(18002390) ||
    ids.Any(helperIds.Contains) || helperIds.Count != pairs.Length + 2 * ids.Length ||
    pairs.Length != ids.Length * (ids.Length - 1) / 2 ||
    pairs.Select(p => (p.Low, p.High)).Distinct().Count() != pairs.Length ||
    pairs.Any(p => p.Low >= p.High || !ids.Contains(p.Low) || !ids.Contains(p.High)) ||
    config.ClearanceRadius <= 0 || config.EligibilityRadius <= config.ClearanceRadius || config.ScoreBias < 0)
    throw new Exception("Invalid destination/helper registry");
var map = MSBE.Read(input);
var options = new JsonSerializerOptions { IncludeFields = true };
string Json(object value) => JsonSerializer.Serialize(value, value.GetType(), options);
object State(MSBE value) => new {
    Map = JsonSerializer.SerializeToElement(value, options),
    Regions = value.Regions.GetEntries().Select(r => new {
        Type = r.GetType().FullName, Data = Json(r), Shape = Json(r.Shape)
    }).ToArray()
};
var before = Json(State(map));
if (editorInput != null && before != Json(State(MSBE.Read(editorInput))))
    throw new Exception("Repository and saved editor maps differ; reconcile before regeneration");
var points = ids.ToDictionary(id => id, id => map.Regions.Others.Single(r => r.EntityID == id));
foreach (var point in points.Values) {
    if (point.Shape is not MSB.Shape.Sphere || !Finite(point.Position) || !Finite(point.Rotation))
        throw new Exception($"Destination {point.EntityID} is not a finite spherical landing marker");
}
var allRegions = map.Regions.GetEntries().ToArray();
var existing = map.Regions.Others.Where(r => helperIds.Contains(r.EntityID)).ToArray();
var existingById = existing.ToDictionary(r => r.EntityID);
if (allRegions.Count(r => helperIds.Contains(r.EntityID)) != existing.Length ||
    existing.Select(r => r.EntityID).Distinct().Count() != existing.Length)
    throw new Exception("Helper ID occurs outside Others or is duplicated");
var ownedNames = pairs.ToDictionary(p => p.RegionId, p => $"Sovereign_Hadeon_Near_{p.Low}_{p.High}");
foreach (var d in config.Destinations) {
    ownedNames.Add(d.ClearanceId, $"Sovereign_Hadeon_Teleport_Clearance_{d.EntityId}");
    ownedNames.Add(d.EligibilityId, $"Sovereign_Hadeon_Vortex_Eligibility_{d.EntityId}");
}
foreach (var region in existing)
    if (region.Name != ownedNames[region.EntityID])
        throw new Exception($"Helper {region.EntityID} is not owned by this registry: {region.Name}");
var newHelpers = helperIds.Except(existing.Select(r => r.EntityID)).ToHashSet();
var withoutHelpers = MSBE.Read(input);
withoutHelpers.Regions.Others.RemoveAll(r => helperIds.Contains(r.EntityID));
var unrelatedBefore = Json(State(withoutHelpers));
var source = File.ReadAllText(eventSource);
// Sources may already contain this recipe's InArea calls; only this exact use is allowed.
foreach (var id in helperIds) {
    var token = new Regex($@"(?<!\d){id}(?!\d)", RegexOptions.CultureInvariant);
    if (token.IsMatch(unrelatedBefore)) throw new Exception($"Helper ID {id} occurs in unrelated map data");
    var nonSelectorSource = Regex.Replace(source,
        $@"InArea\(\s*(10000|18002354)\s*,\s*{id}\s*\)", "", RegexOptions.CultureInvariant);
    if (token.IsMatch(nonSelectorSource)) throw new Exception($"Helper ID {id} has an unexpected source use");
}
// Scan once per binary, not once per helper. Current existing helper references
// are retained; newly allocated IDs must not already occur in native arguments.
foreach (var binary in binaries) {
    foreach (var instruction in EMEVD.Read(binary).Events.SelectMany(e => e.Instructions)) {
        for (var offset = 0; offset + 4 <= instruction.ArgData.Length; offset += 4) {
            var id = BinaryPrimitives.ReadUInt32LittleEndian(instruction.ArgData.AsSpan(offset, 4));
            if (newHelpers.Contains(id)) throw new Exception($"New helper ID {id} already occurs in {binary}");
        }
    }
}
var arena = map.Regions.GetEntries().Single(r => r.EntityID == config.ArenaRegionId);
if (arena.Shape is not MSB.Shape.Box arenaBox || arena.Rotation.X != 0 || arena.Rotation.Z != 0)
    throw new Exception("Arena must be an upright box");
foreach (var point in points.Values)
    if (!InsideBox(arena, point.Position)) throw new Exception($"Destination {point.EntityID} is outside the arena");
var arenaBottom = arena.Position.Y;
var arenaHeight = arenaBox.Height;
// More than the arena diameter on each side of every bisector. No per-frame
// coordinates or distance arithmetic is introduced into the runtime scripts.
var length = Math.Max(1000f, MathF.Sqrt(arenaBox.Width * arenaBox.Width + arenaBox.Depth * arenaBox.Depth) * 4);
Directory.CreateDirectory(output);
var unchanged = Path.Combine(output, "unchanged-map.msb.dcx");
map.Write(unchanged);
if (Json(State(MSBE.Read(unchanged))) != before) throw new Exception("Unchanged native roundtrip failed");

void Put(MSBE.Region.Other region) {
    var index = map.Regions.Others.FindIndex(r => r.EntityID == region.EntityID);
    if (index >= 0) map.Regions.Others[index] = region;
    else map.Regions.Others.Add(region);
}
var pairManifest = new List<object>();
foreach (var pair in pairs) {
    var a = points[pair.Low].Position;
    var b = points[pair.High].Position;
    var delta = new Vector2(b.X - a.X, b.Z - a.Z);
    if (delta.Length() < 0.01f) throw new Exception("Landing markers must differ horizontally by at least 1 cm");
    var normal = Vector2.Normalize(delta);
    var midpoint = (a + b) / 2;
    var tieBias = config.ScoreBias * (Array.IndexOf(ids, pair.High) - Array.IndexOf(ids, pair.Low)) / (2 * delta.Length());
    var region = (MSBE.Region.Other)(existingById.GetValueOrDefault(pair.RegionId) ?? points[pair.Low]).DeepCopy();
    region.EntityID = pair.RegionId;
    region.Name = ownedNames[pair.RegionId];
    region.Position = new(midpoint.X - normal.X * (length / 2 - tieBias), arenaBottom,
        midpoint.Z - normal.Y * (length / 2 - tieBias));
    region.Rotation = new(0, MathF.Atan2(-normal.Y, normal.X) * 180 / MathF.PI, 0);
    region.Shape = new MSB.Shape.Box(length, 2 * length, arenaHeight);
    Put(region);
    pairManifest.Add(new { regionId = pair.RegionId, low = pair.Low, high = pair.High,
        region.Position, region.Rotation, width = length, depth = 2 * length, height = arenaHeight, tieBias });
}
List<object> MakeSpheres(Dictionary<uint, uint> mapping, float radius) {
    var entries = new List<object>();
    foreach (var id in ids) {
        var region = (MSBE.Region.Other)(existingById.GetValueOrDefault(mapping[id]) ?? points[id]).DeepCopy();
        region.Position = points[id].Position;
        region.Rotation = points[id].Rotation;
        region.EntityID = mapping[id];
        region.Name = ownedNames[region.EntityID];
        region.Shape = new MSB.Shape.Sphere(radius);
        Put(region);
        entries.Add(new { region.EntityID, destinationId = id, region.Position, radius });
    }
    return entries;
}
var clearanceManifest = MakeSpheres(clearanceByDestination, config.ClearanceRadius);
var eligibilityManifest = MakeSpheres(eligibilityByDestination, config.EligibilityRadius);
var candidate = Path.Combine(output, "m18_00_00_00.msb.dcx");
map.Write(candidate);
var written = MSBE.Read(candidate);
if (Json(State(written)) != Json(State(map))) throw new Exception("Candidate native roundtrip failed");
var actualHelpers = written.Regions.Others.Where(r => helperIds.Contains(r.EntityID)).ToArray();
if (actualHelpers.Length != helperIds.Count || actualHelpers.Select(r => r.EntityID).Distinct().Count() != helperIds.Count)
    throw new Exception("Candidate helper inventory differs");
var reverse = MSBE.Read(candidate);
reverse.Regions.Others.RemoveAll(r => helperIds.Contains(r.EntityID));
if (Json(State(reverse)) != unrelatedBefore) throw new Exception("Unrelated decoded content changed");
// Restore originals at their original indices, proving order and all authoring
// fields as well as unrelated native content reverse exactly to the input.
var original = MSBE.Read(input);
foreach (var region in existing) {
    var index = original.Regions.Others.FindIndex(r => r.EntityID == region.EntityID);
    reverse.Regions.Others.Insert(index, (MSBE.Region.Other)region.DeepCopy());
}
if (Json(State(reverse)) != before) throw new Exception("Original map did not reverse-preserve");
var boxByPair = pairs.ToDictionary(p => (p.Low, p.High),
    p => written.Regions.Others.Single(r => r.EntityID == p.RegionId));
var clearanceSpheres = ids.ToDictionary(id => id, id => written.Regions.Others.Single(r => r.EntityID == clearanceByDestination[id]));
var eligibilitySpheres = ids.ToDictionary(id => id, id => written.Regions.Others.Single(r => r.EntityID == eligibilityByDestination[id]));
foreach (var id in ids) {
    if (clearanceSpheres[id].Position != points[id].Position || eligibilitySpheres[id].Position != points[id].Position)
        throw new Exception($"Sphere center drift for {id}");
    foreach (var region in new[] { clearanceSpheres[id], eligibilitySpheres[id] }) {
        var radius = ((MSB.Shape.Sphere)region.Shape).Radius;
        foreach (var axis in new[] { Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ })
            if (!InsideSphere(region, region.Position + axis * (radius - 0.001f)) ||
                InsideSphere(region, region.Position + axis * (radius + 0.001f)))
                throw new Exception($"Sphere boundary failed for {region.EntityID}");
    }
}
var heights = new[] { points.Values.Min(p => p.Position.Y) - 2, points.Values.Min(p => p.Position.Y),
    points.Values.Max(p => p.Position.Y), points.Values.Max(p => p.Position.Y) + 2 };
foreach (var pair in pairs) {
    var a = points[pair.Low].Position;
    var b = points[pair.High].Position;
    var normal = Vector2.Normalize(new(b.X - a.X, b.Z - a.Z));
    var midpoint = (a + b) / 2;
    var offset = new Vector3(normal.X, 0, normal.Y) * 0.05f;
    foreach (var height in heights) {
        midpoint.Y = height;
        if (!InsideBox(boxByPair[(pair.Low, pair.High)], midpoint - offset) ||
            InsideBox(boxByPair[(pair.Low, pair.High)], midpoint + offset))
            throw new Exception($"Pair {pair.RegionId} fails bisector-side check at height {height}");
    }
}
float HorizontalDistance(Vector3 position, uint id) {
    var point = points[id].Position;
    return Vector2.Distance(new(position.X, position.Z), new(point.X, point.Z));
}
bool Eligible(uint id, Vector3 player, Vector3? boss, bool vortex) =>
    !InsideSphere(clearanceSpheres[id], player) &&
    (boss == null || !InsideSphere(clearanceSpheres[id], boss.Value)) &&
    (!vortex || InsideSphere(eligibilitySpheres[id], player));
uint? Select(Vector3 player, Vector3? boss, bool vortex) {
    uint? winner = null;
    foreach (var id in ids) {
        if (!Eligible(id, player, boss, vortex)) continue;
        if (winner == null || !InsideBox(boxByPair[(winner.Value, id)], player)) winner = id;
    }
    return winner;
}
var maximumError = 0f;
void CheckSelection(Vector3 player, Vector3? boss = null, bool vortex = false) {
    var actual = Select(player, boss, vortex);
    var nearest = ids.Where(id => Eligible(id, player, boss, vortex))
        .OrderBy(id => HorizontalDistance(player, id)).ThenBy(id => id).Cast<uint?>().FirstOrDefault();
    if (actual == null || nearest == null) {
        if (actual != nearest) throw new Exception("Eligibility mismatch");
        return;
    }
    var error = HorizontalDistance(player, actual.Value) - HorizontalDistance(player, nearest.Value);
    maximumError = Math.Max(maximumError, error);
    if (error > 0.001f) throw new Exception($"Nearest selection error at {player}: {actual} vs {nearest}, {error}m");
}
var gridSamples = 0;
foreach (var height in heights)
for (var x = -10f; x <= 90f; x += 0.5f)
for (var z = 100f; z <= 200f; z += 0.5f) {
    var player = new Vector3(x, height, z);
    CheckSelection(player);
    CheckSelection(player, points[ids[gridSamples % ids.Length]].Position, false);
    CheckSelection(player, points[ids[gridSamples % ids.Length]].Position, true);
    gridSamples++;
}
var junctionSamples = 0;
for (var i = 0; i < ids.Length; i++)
for (var j = i + 1; j < ids.Length; j++)
for (var k = j + 1; k < ids.Length; k++) {
    var a = points[ids[i]].Position;
    var b = points[ids[j]].Position;
    var c = points[ids[k]].Position;
    var ab = new Vector2(b.X - a.X, b.Z - a.Z);
    var ac = new Vector2(c.X - a.X, c.Z - a.Z);
    var determinant = ab.X * ac.Y - ab.Y * ac.X;
    if (Math.Abs(determinant) < 0.001f) continue;
    var rightB = (b.X * b.X + b.Z * b.Z - a.X * a.X - a.Z * a.Z) / 2;
    var rightC = (c.X * c.X + c.Z * c.Z - a.X * a.X - a.Z * a.Z) / 2;
    var center = new Vector2((rightB * ac.Y - ab.Y * rightC) / determinant,
        (ab.X * rightC - rightB * ac.X) / determinant);
    if (center.X < -10 || center.X > 90 || center.Y < 100 || center.Y > 200) continue;
    foreach (var height in heights)
    for (var dx = -2; dx <= 2; dx++)
    for (var dz = -2; dz <= 2; dz++) {
        CheckSelection(new(center.X + dx * 0.00025f, height, center.Y + dz * 0.00025f));
        junctionSamples++;
    }
}
if (inputs.Any(entry => Hash(entry.Key) != entry.Value)) throw new Exception("An input changed during generation");
File.WriteAllText(Path.Combine(output, "regions.json"), JsonSerializer.Serialize(new {
    schemaVersion = 1,
    destinations = ids.Select(id => new { EntityID = id, points[id].Position, points[id].Rotation }),
    pairRegions = pairManifest, clearanceRegions = clearanceManifest, eligibilityRegions = eligibilityManifest,
    nearestMetric = "horizontal", clearanceMetric = "three-dimensional", scoreBias = config.ScoreBias
}, new JsonSerializerOptions { WriteIndented = true, IncludeFields = true }));
File.WriteAllText(Path.Combine(output, "manifest.json"), JsonSerializer.Serialize(new {
    input, inputSha256 = inputs[input], editorInput, editorSha256 = editorInput == null ? null : inputs[editorInput],
    inputs, candidate, candidateSha256 = Hash(candidate), unchangedRoundtrip = unchanged,
    destinations = ids.Select(id => new { EntityID = id, points[id].Position, points[id].Rotation }),
    pairRegions = pairManifest, clearanceRegions = clearanceManifest, eligibilityRegions = eligibilityManifest,
    helperCount = helperIds.Count, addedHelpers = newHelpers.Count, retainedHelperIds = existing.Select(r => r.EntityID),
    updatedHelperIds = existing.Where(r => Json(r) != Json(written.Regions.Others.Single(w => w.EntityID == r.EntityID)) ||
        Json(r.Shape) != Json(written.Regions.Others.Single(w => w.EntityID == r.EntityID).Shape)).Select(r => r.EntityID),
    nearestMetric = "horizontal", clearanceMetric = "three-dimensional", scoreBias = config.ScoreBias,
    geometrySamples = gridSamples, selectionChecks = gridSamples * 3 + junctionSamples, junctionSamples,
    maximumNearestErrorMeters = maximumError, nearestErrorLimitMeters = 0.001f,
    decodedRoundtrip = true, unrelatedDecodedEntriesPreserved = true, originalRepositoryMapReversePreserved = true,
    gameplayVerified = false, boxContainmentConventionRequiresGameCheck = true
}, new JsonSerializerOptions { WriteIndented = true, IncludeFields = true }));
Console.WriteLine($"Validated {ids.Length} destinations, {pairs.Length} pairs and {ids.Length * 2} spheres; " +
    $"{gridSamples * 3 + junctionSamples} selection checks, maximum error {maximumError * 1000:F3} mm; unrelated decoded data preserved.");

static bool Finite(Vector3 v) => float.IsFinite(v.X) && float.IsFinite(v.Y) && float.IsFinite(v.Z);
static string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();
static bool InsideSphere(MSBE.Region region, Vector3 position) =>
    Vector3.Distance(position, region.Position) <= ((MSB.Shape.Sphere)region.Shape).Radius;
static bool InsideBox(MSBE.Region region, Vector3 position) {
    var box = (MSB.Shape.Box)region.Shape;
    var radians = region.Rotation.Y * MathF.PI / 180;
    var offset = position - region.Position;
    var localX = MathF.Cos(radians) * offset.X - MathF.Sin(radians) * offset.Z;
    var localZ = MathF.Sin(radians) * offset.X + MathF.Cos(radians) * offset.Z;
    return Math.Abs(localX) <= box.Width / 2 && Math.Abs(localZ) <= box.Depth / 2 &&
        position.Y >= region.Position.Y && position.Y <= region.Position.Y + box.Height;
}
record Configuration(int SchemaVersion, uint ArenaRegionId, float ClearanceRadius, float EligibilityRadius,
    float ScoreBias, Destination[] Destinations, Pair[] PairRegions);
record Destination(uint EntityId, uint ClearanceId, uint EligibilityId);
record Pair(uint Low, uint High, uint RegionId);
