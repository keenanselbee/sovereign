using SoulsFormats;
using System.Numerics;
using System.Security.Cryptography;
using System.Text.Json;
using System.Text.RegularExpressions;

// Expand the eight existing eligibility spheres in an isolated map candidate.
if (args.Length != 5) throw new ArgumentException(
    "repo-map editor-map candidate-directory Smithbox-tools event-source.js");
var input = Path.GetFullPath(args[0]);
var editorInput = Path.GetFullPath(args[1]);
var output = Path.GetFullPath(args[2]);
var library = Path.GetFullPath(args[3]);
var eventSource = Path.GetFullPath(args[4]);
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
foreach (var path in new[] { input, editorInput, eventSource })
    if (!File.Exists(path)) throw new FileNotFoundException("A required input is missing", path);
Directory.SetCurrentDirectory(library);

const float previousRadius = 6f;
const float radius = 8f;
const float clearanceRadius = 2.5f;
uint[] destinations = [18002368, 18002369, 18002370, 18002371,
    18002372, 18002373, 18002381, 18002382];
uint[] eligibilityIds = [18005936, 18005937, 18005938, 18005939,
    18005940, 18005941, 18005942, 18005943];
uint[] clearanceIds = [18005915, 18005916, 18005917, 18005918,
    18005919, 18005920, 18005934, 18005935];
var inputHash = Hash(input);
var editorHash = Hash(editorInput);
var sourceHash = Hash(eventSource);
var options = new JsonSerializerOptions { IncludeFields = true };
string Json(object value) => JsonSerializer.Serialize(value, value.GetType(), options);
object State(MSBE map) => new {
    Map = JsonSerializer.SerializeToElement(map, options),
    Regions = map.Regions.GetEntries().Select(region => new {
        Type = region.GetType().FullName, Data = Json(region), Shape = Json(region.Shape)
    }).ToArray()
};
var map = MSBE.Read(input);
if (Json(State(map)) != Json(State(MSBE.Read(editorInput))))
    throw new Exception("Repository and saved editor maps differ in decoded content");
var before = Json(State(map));
var allRegions = map.Regions.GetEntries().ToArray();
foreach (var id in Enumerable.Range(18005900, 36).Select(n => (uint)n))
    if (allRegions.Count(region => region.EntityID == id) != 1)
        throw new Exception($"Retained teleport helper {id} is missing or duplicated");
foreach (var id in eligibilityIds)
    if (allRegions.Count(region => region.EntityID == id) != 1)
        throw new Exception($"Existing eligibility region {id} is missing or duplicated");
var source = File.ReadAllText(eventSource);
foreach (var id in eligibilityIds) {
    // The event controller may already contain its planned membership checks.
    var unrelatedSource = Regex.Replace(source, $@"InArea\(\s*10000\s*,\s*{id}\s*\)", "",
        RegexOptions.CultureInvariant);
    if (Regex.IsMatch(unrelatedSource, $@"(?<!\d){id}(?!\d)", RegexOptions.CultureInvariant))
        throw new Exception($"Eligibility ID {id} has an unexpected event-source use");
}

var regions = new List<object>();
for (var index = 0; index < destinations.Length; index++) {
    var destination = map.Regions.Others.Single(region => region.EntityID == destinations[index]);
    var clearance = map.Regions.Others.Single(region => region.EntityID == clearanceIds[index]);
    if (destination.Shape is not MSB.Shape.Sphere ||
        clearance.Shape is not MSB.Shape.Sphere sphere ||
        Math.Abs(sphere.Radius - clearanceRadius) > 0.0001f ||
        Vector3.Distance(destination.Position, clearance.Position) > 0.001f)
        throw new Exception($"Destination or clearance geometry changed for {destinations[index]}");
    var eligibility = map.Regions.Others.Single(region => region.EntityID == eligibilityIds[index]);
    if (eligibility.Name != $"Sovereign_Hadeon_Vortex_Eligibility_{destinations[index]}" ||
        eligibility.Shape is not MSB.Shape.Sphere existingSphere ||
        Math.Abs(existingSphere.Radius - previousRadius) > 0.0001f ||
        Vector3.Distance(eligibility.Position, destination.Position) > 0.001f)
        throw new Exception($"Existing eligibility geometry changed for {destinations[index]}");
    eligibility.Shape = new MSB.Shape.Sphere(radius);
    regions.Add(new { eligibilityId = eligibility.EntityID, destinationId = destination.EntityID,
        clearanceId = clearance.EntityID, eligibility.Position, radius, clearanceRadius });
}

Directory.CreateDirectory(output);
var unchanged = Path.Combine(output, "unchanged-map.msb.dcx");
var original = MSBE.Read(input);
original.Write(unchanged);
if (Json(State(MSBE.Read(unchanged))) != before)
    throw new Exception("Unchanged native roundtrip changed decoded map content");
var candidate = Path.Combine(output, "m18_00_00_00.msb.dcx");
map.Write(candidate);
var readback = MSBE.Read(candidate);
if (Json(State(readback)) != Json(State(map)))
    throw new Exception("Candidate native roundtrip changed decoded map content");
foreach (var id in eligibilityIds)
    if (readback.Regions.Others.Count(region => region.EntityID == id) != 1)
        throw new Exception($"Eligibility region {id} is missing or duplicated");
var shellSamples = 0;
for (var index = 0; index < destinations.Length; index++) {
    var destination = readback.Regions.Others.Single(region => region.EntityID == destinations[index]);
    var eligibility = readback.Regions.Others.Single(region => region.EntityID == eligibilityIds[index]);
    var clearance = readback.Regions.Others.Single(region => region.EntityID == clearanceIds[index]);
    if (eligibility.Shape is not MSB.Shape.Sphere eligibilitySphere ||
        clearance.Shape is not MSB.Shape.Sphere clearanceSphere ||
        Math.Abs(eligibilitySphere.Radius - radius) > 0.0001f ||
        Vector3.Distance(eligibility.Position, destination.Position) > 0.001f)
        throw new Exception($"Eligibility center/radius changed for {destinations[index]}");
    foreach (var axis in new[] { Vector3.UnitX, -Vector3.UnitX, Vector3.UnitZ, -Vector3.UnitZ })
    foreach (var distance in new[] { 2.51f, 6.01f, 7.99f }) {
        var point = destination.Position + axis * distance;
        if (Vector3.Distance(point, eligibility.Position) >= eligibilitySphere.Radius ||
            Vector3.Distance(point, clearance.Position) <= clearanceSphere.Radius)
            throw new Exception($"Eligibility shell failed at {destinations[index]}, distance {distance}");
        shellSamples++;
    }
    foreach (var axis in new[] { Vector3.UnitX, -Vector3.UnitX, Vector3.UnitZ, -Vector3.UnitZ }) {
        var outside = destination.Position + axis * 8.01f;
        if (Vector3.Distance(outside, eligibility.Position) <= eligibilitySphere.Radius)
            throw new Exception($"Eligibility outer boundary failed at {destinations[index]}");
        shellSamples++;
    }
}
foreach (var id in eligibilityIds)
    readback.Regions.Others.Single(region => region.EntityID == id).Shape = new MSB.Shape.Sphere(previousRadius);
if (Json(State(readback)) != before)
    throw new Exception("Candidate changed content other than the eight eligibility radii");
if (Hash(input) != inputHash || Hash(editorInput) != editorHash || Hash(eventSource) != sourceHash)
    throw new Exception("An input changed during candidate generation");
File.WriteAllText(Path.Combine(output, "manifest.json"), JsonSerializer.Serialize(new {
    input, inputSha256 = inputHash, editorInput, editorSha256 = editorHash,
    eventSource, eventSourceSha256 = sourceHash,
    candidate, candidateSha256 = Hash(candidate), unchangedRoundtrip = unchanged,
    regions, preservedPairSelectors = "18005900-18005933",
    preservedClearanceRegions = "18005915-18005920, 18005934-18005935",
    decodedRoundtrip = true, unrelatedDecodedMapContentPreserved = true,
    shellSamples,
    previousRadius, trialRadius = radius,
    radiusCaveat = "Diagnostic 8 m eligibility trial only. The 2.5 m clearance and slam hitbox are unchanged; reach requires in-game calibration.",
    gameplayVerified = false
}, new JsonSerializerOptions { WriteIndented = true, IncludeFields = true }));
Console.WriteLine($"Validated {regions.Count} expanded eligibility spheres, {shellSamples} shell samples and full decoded map preservation.");

static string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();
