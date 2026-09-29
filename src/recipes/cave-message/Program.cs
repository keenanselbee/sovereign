using SoulsFormats;
using System.Numerics;
using System.Security.Cryptography;
using System.Text.Json;

if (args.Length != 4) throw new ArgumentException(
    "repo-map editor-map candidate-directory Smithbox-tools");
var input = Path.GetFullPath(args[0]);
var editorInput = Path.GetFullPath(args[1]);
var output = Path.GetFullPath(args[2]);
var library = Path.GetFullPath(args[3]);
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
foreach (var path in new[] { input, editorInput })
    if (!File.Exists(path)) throw new FileNotFoundException("A required map is missing", path);
Directory.SetCurrentDirectory(library);

var inputHash = Hash(input);
var editorHash = Hash(editorInput);
var options = new JsonSerializerOptions { IncludeFields = true };
string Json(object value) => JsonSerializer.Serialize(value, value.GetType(), options);
object State(MSBE map) => new {
    Map = JsonSerializer.SerializeToElement(map, options),
    Regions = map.Regions.GetEntries().Select(region => new {
        Type = region.GetType().FullName, Data = Json(region), Shape = Json(region.Shape)
    }).ToArray()
};

var map = MSBE.Read(input);
var originalState = Json(State(map));
if (originalState != Json(State(MSBE.Read(editorInput))))
    throw new Exception("Repository and saved editor maps differ in decoded content");
var messages = map.Regions.Messages;
if (messages.Count != 1) throw new Exception("Expected exactly one message region in m18");
var message = messages.Single();
if (message.RegionID != 100 || message.MessageID != 2020 ||
    message.MessageSfxID != 30 || message.Hidden || message.EnableEventFlagID != 0 ||
    message.ItemLotParamID != -1 || message.Name != "ヒント血文字：チュートリアル導線" ||
    Vector3.Distance(message.Position, new Vector3(-60.28f, 5.77f, 25.11f)) > 0.01f)
    throw new Exception("The Cave of Knowledge ground message no longer matches the reviewed target");

Directory.CreateDirectory(output);
var unchanged = Path.Combine(output, "unchanged-map.msb.dcx");
map.Write(unchanged);
if (Json(State(MSBE.Read(unchanged))) != originalState)
    throw new Exception("Unchanged native roundtrip changed decoded map content");

messages.Remove(message);
var expectedState = Json(State(map));
var candidate = Path.Combine(output, "m18_00_00_00.msb.dcx");
map.Write(candidate);
var readback = MSBE.Read(candidate);
if (Json(State(readback)) != expectedState)
    throw new Exception("Candidate native roundtrip changed decoded map content");
if (readback.Regions.Messages.Count != 0)
    throw new Exception("The cave ground message remains in the candidate");
map.Regions.Messages.Add(message);
if (Json(State(map)) != originalState)
    throw new Exception("Candidate changed map content beyond the single Message region");
if (Hash(input) != inputHash || Hash(editorInput) != editorHash)
    throw new Exception("A map input changed during candidate generation");

File.WriteAllText(Path.Combine(output, "manifest.json"), JsonSerializer.Serialize(new {
    input, inputSha256 = inputHash, editorInput, editorSha256 = editorHash,
    candidate, candidateSha256 = Hash(candidate), unchangedRoundtrip = unchanged,
    removedRegionId = message.RegionID, removedMessageId = message.MessageID,
    removedMessageSfxId = message.MessageSfxID,
    removedPosition = message.Position,
    decodedRoundtrip = true, unrelatedDecodedMapContentPreserved = true,
    gameplayVerified = false
}, new JsonSerializerOptions { WriteIndented = true, IncludeFields = true }));
Console.WriteLine("Validated removal of Message region 100/2020 and full decoded map preservation.");

static string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();
