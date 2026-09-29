using SoulsFormats;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text.Json;

if (args.Length != 3)
    throw new ArgumentException("c2500.anibnd.dcx new-output-directory Smithbox-directory");
var input = Path.GetFullPath(args[0]);
var output = Path.GetFullPath(args[1]);
var library = Path.GetFullPath(args[2]);
if (Directory.Exists(output)) throw new IOException("Use a new output directory");
AssemblyLoadContext.Default.Resolving += (context, name) => {
    var path = Path.Combine(library, name.Name + ".dll");
    return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(library);
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)));
var inputHash = Hash(input);
var binder = BND4.Read(input);
var timelineMember = binder.Files.Single(file => file.Name.EndsWith(".tae"));
var timeline = TAE.Read(timelineMember.Bytes);
if (timeline.Animations.Count != 282 || timeline.Animations.Select(a => a.ID).Distinct().Count() != 282)
    throw new InvalidOperationException("Expected the accepted 278 native and four private TAE records");
var native = timeline.Animations.Single(a => a.ID == 3028);
if (native.Events.Count != 62 || native.Events.Count(e => e.Type == 2 && Math.Abs(e.StartTime - 2.6666667f) < 0.0001f) != 1)
    throw new InvalidOperationException("Native 3028 impact or event count changed");

string Describe(TAE.Animation animation) => JsonSerializer.Serialize(new {
    animation.ID, animation.AnimFileName,
    header = animation.MiniHeader is TAE.Animation.AnimMiniHeader.Standard standard
        ? new { type = "Standard", standard.ImportsHKX, standard.ImportHKXSourceAnimID,
            standard.IsLoopByDefault, standard.AllowDelayLoad }
        : new { type = animation.MiniHeader.GetType().Name, ImportsHKX = false,
            ImportHKXSourceAnimID = 0, IsLoopByDefault = false, AllowDelayLoad = false },
    groups = animation.EventGroups.Select(group => new { group.GroupType,
        group.GroupData.DataType, group.GroupData.CutsceneEntityType,
        group.GroupData.CutsceneEntityIDPart1, group.GroupData.CutsceneEntityIDPart2,
        group.GroupData.Area, group.GroupData.Block }),
    events = animation.Events.Select(item => new { item.Type, item.Unk04, item.StartTime, item.EndTime,
        groupIndex = item.Group == null ? -1 : animation.EventGroups.IndexOf(item.Group),
        parameters = Convert.ToHexString(item.GetParameterBytes(false)) })
});
var untouched = timeline.Animations.Where(a => a.ID < 3030 || a.ID > 3033)
    .ToDictionary(a => a.ID, Describe);
var oldRates = new[] { 1f, 4f / 3f, 5f / 3f, 2f };
var newRates = new[] { 2f, 7f / 3f, 8f / 3f, 3f };
const float impact = 2.6666667f;
var expected = new Dictionary<long, string>();
var tierDetails = new List<object>();
for (var index = 0; index < 4; index++) {
    var id = 3030 + index;
    var animation = timeline.Animations.Single(a => a.ID == id);
    var header = animation.MiniHeader as TAE.Animation.AnimMiniHeader.Standard;
    if (header == null || !header.ImportsHKX || header.ImportHKXSourceAnimID != 3028
        || animation.AnimFileName != native.AnimFileName || animation.Events.Count != 65)
        throw new InvalidOperationException($"Private route {id} changed motion or event count");
    var speed = animation.Events.Single(e => e.Type == 608);
    var live = animation.Events.Single(e => e.Type == 67 && BitConverter.ToInt32(e.GetParameterBytes(false), 0) == 1627600);
    var cue = animation.Events.Single(e => e.Type == 67 && BitConverter.ToInt32(e.GetParameterBytes(false), 0) == 1627601);
    var speedBytes = speed.GetParameterBytes(false);
    if (speedBytes.Length != 16 || speed.StartTime != 0f || speed.EndTime != 5f
        || BitConverter.ToSingle(speedBytes, 0) != oldRates[index]
        || BitConverter.ToSingle(speedBytes, 4) != oldRates[index]
        || live.StartTime != 0f || live.EndTime != 5f
        || Math.Abs(cue.StartTime - (impact - oldRates[index])) > 0.0001f
        || Math.Abs(cue.EndTime - cue.StartTime - oldRates[index] * 0.1f) > 0.0001f)
        throw new InvalidOperationException($"Private route {id} is not the reviewed prior tier");
    for (var eventIndex = 0; eventIndex < native.Events.Count; eventIndex++) {
        var before = native.Events[eventIndex];
        var after = animation.Events[eventIndex];
        var bytes = before.GetParameterBytes(false);
        var copied = after.GetParameterBytes(false);
        if (before.Type != after.Type || before.Unk04 != after.Unk04
            || before.StartTime != after.StartTime || before.EndTime != after.EndTime
            || copied.Length < bytes.Length || !copied.AsSpan(0, bytes.Length).SequenceEqual(bytes)
            || copied.AsSpan(bytes.Length).ToArray().Any(value => value != 0))
            throw new InvalidOperationException($"Private route {id} source event {eventIndex} changed");
    }
    var rate = newRates[index];
    BitConverter.GetBytes(rate).CopyTo(speedBytes, 0);
    BitConverter.GetBytes(rate).CopyTo(speedBytes, 4);
    speed.SetParameterBytes(false, speedBytes, false);
    cue.StartTime = Math.Max(0f, impact - rate);
    cue.EndTime = cue.StartTime + 0.1f * rate;
    expected[id] = Describe(animation);
    tierDetails.Add(new { animationId = id, speed = rate, impactTimelineSeconds = impact,
        cueTimelineSeconds = cue.StartTime, cueEndTimelineSeconds = cue.EndTime,
        cueToImpactRealSeconds = (impact - cue.StartTime) / rate });
}

timelineMember.Bytes = timeline.Write();
Directory.CreateDirectory(output);
var candidatePath = Path.Combine(output, "c2500.anibnd.dcx");
binder.Write(candidatePath);
var readbackBinder = BND4.Read(candidatePath);
var originalBinder = BND4.Read(input);
if (originalBinder.Files.Count != readbackBinder.Files.Count || originalBinder.Version != readbackBinder.Version
    || originalBinder.Compression != readbackBinder.Compression || originalBinder.Format != readbackBinder.Format
    || originalBinder.BigEndian != readbackBinder.BigEndian || originalBinder.BitBigEndian != readbackBinder.BitBigEndian
    || originalBinder.Unicode != readbackBinder.Unicode || originalBinder.Extended != readbackBinder.Extended)
    throw new InvalidOperationException("Binder metadata drift");
for (var index = 0; index < originalBinder.Files.Count; index++) {
    var before = originalBinder.Files[index];
    var after = readbackBinder.Files[index];
    if (before.Name != after.Name || before.ID != after.ID || before.Flags != after.Flags
        || before.CompressionType != after.CompressionType)
        throw new InvalidOperationException("Binder member metadata drift");
    if (before.ID != timelineMember.ID && !before.Bytes.Span.SequenceEqual(after.Bytes.Span))
        throw new InvalidOperationException($"Unrelated binder member changed: {before.Name}");
}
var readback = TAE.Read(readbackBinder.Files.Single(f => f.ID == timelineMember.ID).Bytes);
if (readback.Animations.Count != 282) throw new InvalidOperationException("Animation count drift");
foreach (var animation in readback.Animations) {
    var signature = Describe(animation);
    if (animation.ID is >= 3030 and <= 3033) {
        if (signature != expected[animation.ID]) throw new InvalidOperationException($"Route {animation.ID} readback drift");
    } else if (signature != untouched[animation.ID]) {
        throw new InvalidOperationException($"Original animation {animation.ID} changed");
    }
}
if (Hash(input) != inputHash) throw new InvalidOperationException("Input changed during retune");
var validation = new { input, inputHash, candidatePath, candidateHash = Hash(candidatePath),
    tiers = tierDetails, preservedOtherBinderMembers = true, preservedOtherTimelineRecords = true,
    behaviorGraphChanged = false, gameTested = false };
File.WriteAllText(Path.Combine(output, "validation.json"),
    JsonSerializer.Serialize(validation, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine("Verified four retuned private routes and preserved all other binder members and TAE records.");
