using SoulsFormats;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text.Json;

if (args.Length == 4 && args[0] == "extract-graph") {
    var archiveInput = Path.GetFullPath(args[1]);
    var destination = Path.GetFullPath(args[2]);
    var library = Path.GetFullPath(args[3]);
    if (File.Exists(destination)) throw new IOException("Use a new graph extraction path");
    AssemblyLoadContext.Default.Resolving += (context, name) => {
        var path = Path.Combine(library, name.Name + ".dll");
        return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
    };
    Directory.SetCurrentDirectory(library);
    var graph = BND4.Read(archiveInput).Files.Single(file => file.ID == 7000501 && file.Name.EndsWith("c9997.hkx"));
    Directory.CreateDirectory(Path.GetDirectoryName(destination)!);
    File.WriteAllBytes(destination, graph.Bytes.ToArray());
    Console.WriteLine($"Extracted {graph.Name} to {destination}");
    return;
}
if (args.Length != 5)
    throw new ArgumentException("c2500.anibnd.dcx c2500.behbnd.dcx candidate-graph.hkx output-directory Smithbox-directory");
var animationInput = Path.GetFullPath(args[0]);
var behaviorInput = Path.GetFullPath(args[1]);
var graphInput = Path.GetFullPath(args[2]);
var output = Path.GetFullPath(args[3]);
var lib = Path.GetFullPath(args[4]);
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
AssemblyLoadContext.Default.Resolving += (context, name) => {
    var path = Path.Combine(lib, name.Name + ".dll");
    return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(lib);
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)));
var animationHash = Hash(animationInput);
var behaviorHash = Hash(behaviorInput);
var graphHash = Hash(graphInput);
var animationBinder = BND4.Read(animationInput);
var behaviorBinder = BND4.Read(behaviorInput);
var timelineMember = animationBinder.Files.Single(file => file.Name.EndsWith(".tae"));
var graphMember = behaviorBinder.Files.Single(file => file.ID == 7000501 && file.Name.EndsWith("c9997.hkx"));
var originalTimeline = TAE.Read(timelineMember.Bytes);
var originalAnimationIds = originalTimeline.Animations.Select(animation => animation.ID).ToHashSet();
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
var originalRecordSignatures = originalTimeline.Animations.ToDictionary(animation => animation.ID, Describe);
var source = originalTimeline.Animations.Single(animation => animation.ID == 3028);
if (source.Events.Count != 62 || source.Events.Count(e => e.Type == 2 && Math.Abs(e.StartTime - 2.6666667f) < 0.0001f) != 1)
    throw new Exception("The reviewed spin-slam source has changed");
if (Enumerable.Range(3030, 4).Any(id => originalAnimationIds.Contains(id)))
    throw new Exception("Private animation ID collision");

var tiers = new[] { 2f, 7f / 3f, 8f / 3f, 3f };
var expected = new List<object>();
for (var index = 0; index < tiers.Length; index++) {
    var animationId = 3030 + index;
    var rate = tiers[index];
    var privateAnimation = new TAE.Animation(animationId, new TAE.Animation.AnimMiniHeader.Standard {
        ImportsHKX = true,
        ImportHKXSourceAnimID = 3028,
        IsLoopByDefault = false,
        AllowDelayLoad = false
    }, source.AnimFileName);
    // The SoulsFormats constructor normalizes some native event payloads with
    // trailing zero extensions. Reuse unchanged event/group objects instead.
    privateAnimation.EventGroups.AddRange(source.EventGroups);
    privateAnimation.Events.AddRange(source.Events);
    void AddEvent(int type, float start, float end, byte[] data) {
        var group = new TAE.EventGroup(type);
        privateAnimation.EventGroups.Add(group);
        privateAnimation.Events.Add(new TAE.Event(start, end, type, 0, data, false) { Group = group });
    }
    var speedData = new byte[16];
    BitConverter.GetBytes(rate).CopyTo(speedData, 0);
    BitConverter.GetBytes(rate).CopyTo(speedData, 4);
    AddEvent(608, 0f, 5f, speedData);
    var liveData = new byte[16];
    BitConverter.GetBytes(1627600).CopyTo(liveData, 0);
    AddEvent(67, 0f, 5f, liveData);
    var cueStart = Math.Max(0f, 2.6666667f - rate);
    var cueEnd = cueStart + rate * 0.1f;
    var cueData = new byte[16];
    BitConverter.GetBytes(1627601).CopyTo(cueData, 0);
    AddEvent(67, cueStart, cueEnd, cueData);
    originalTimeline.Animations.Add(privateAnimation);
    expected.Add(new { animationId, speed = rate, sourceMotion = 3028, groundImpactTimeline = 2.6666667,
        cueTimeline = cueStart, cueEndTimeline = cueEnd, cueToImpactRealSeconds = (2.6666667f - cueStart) / rate,
        markers = new[] { 1627600, 1627601 } });
}
timelineMember.Bytes = originalTimeline.Write();
graphMember.Bytes = File.ReadAllBytes(graphInput);
Directory.CreateDirectory(output);
var animationCandidate = Path.Combine(output, "c2500.anibnd.dcx");
var behaviorCandidate = Path.Combine(output, "c2500.behbnd.dcx");
animationBinder.Write(animationCandidate);
behaviorBinder.Write(behaviorCandidate);

void VerifyBinder(BND4 baseline, BND4 candidate, int changedId) {
    if (baseline.Files.Count != candidate.Files.Count || baseline.Version != candidate.Version
        || baseline.Compression != candidate.Compression || baseline.Format != candidate.Format
        || baseline.BigEndian != candidate.BigEndian || baseline.BitBigEndian != candidate.BitBigEndian
        || baseline.Unicode != candidate.Unicode || baseline.Extended != candidate.Extended)
        throw new Exception("Binder metadata drift");
    for (var i = 0; i < baseline.Files.Count; i++) {
        var a = baseline.Files[i]; var b = candidate.Files[i];
        if (a.Name != b.Name || a.ID != b.ID || a.Flags != b.Flags || a.CompressionType != b.CompressionType)
            throw new Exception("Member metadata drift");
        if (a.ID != changedId && !a.Bytes.Span.SequenceEqual(b.Bytes.Span))
            throw new Exception($"Unrelated member changed: {a.Name}");
    }
}
var animationReadback = BND4.Read(animationCandidate);
var behaviorReadback = BND4.Read(behaviorCandidate);
VerifyBinder(BND4.Read(animationInput), animationReadback, timelineMember.ID);
VerifyBinder(BND4.Read(behaviorInput), behaviorReadback, graphMember.ID);
var timelineReadback = TAE.Read(animationReadback.Files.Single(f => f.ID == timelineMember.ID).Bytes);
if (timelineReadback.Animations.Count != originalAnimationIds.Count + 4
    || !timelineReadback.Animations.Select(a => a.ID).ToHashSet().SetEquals(originalAnimationIds.Concat(Enumerable.Range(3030, 4).Select(i => (long)i))))
    throw new Exception("Animation IDs changed unexpectedly");
foreach (var animation in timelineReadback.Animations.Where(animation => originalAnimationIds.Contains(animation.ID)))
    if (Describe(animation) != originalRecordSignatures[animation.ID])
        throw new Exception($"Original animation {animation.ID} changed");
var paddedEvents = 0;
foreach (var (id, speed) in Enumerable.Range(3030, 4).Zip(tiers)) {
    var animation = timelineReadback.Animations.Single(a => a.ID == id);
    var header = animation.MiniHeader as TAE.Animation.AnimMiniHeader.Standard;
    if (header == null || !header.ImportsHKX || header.ImportHKXSourceAnimID != 3028
        || animation.Events.Count != source.Events.Count + 3)
        throw new Exception($"Private animation {id} lost motion or events");
    var gradient = animation.Events.Single(e => e.Type == 608);
    if (gradient.StartTime != 0f || gradient.EndTime != 5f
        || BitConverter.ToSingle(gradient.GetParameterBytes(false), 0) != speed
        || BitConverter.ToSingle(gradient.GetParameterBytes(false), 4) != speed)
        throw new Exception($"Private animation {id} speed changed");
    var markers = animation.Events.Where(e => e.Type == 67 && BitConverter.ToInt32(e.GetParameterBytes(false), 0) is 1627600 or 1627601).ToArray();
    if (markers.Length != 2) throw new Exception($"Private animation {id} marker count changed");
    var live = markers.Single(e => BitConverter.ToInt32(e.GetParameterBytes(false), 0) == 1627600);
    var cue = markers.Single(e => BitConverter.ToInt32(e.GetParameterBytes(false), 0) == 1627601);
    if (live.StartTime != 0f || live.EndTime != 5f
        || Math.Abs(cue.StartTime - Math.Max(0f, 2.6666667f - speed)) > 0.0001f
        || Math.Abs(cue.EndTime - cue.StartTime - 0.1f * speed) > 0.0001f)
        throw new Exception($"Private animation {id} marker timing changed");
    if (animation.EventGroups.Count != source.EventGroups.Count + 3)
        throw new Exception($"Private animation {id} event groups changed");
    for (var i = 0; i < source.Events.Count; i++) {
        var reference = source.Events[i]; var actual = animation.Events[i];
        var referenceBytes = reference.GetParameterBytes(false);
        var actualBytes = actual.GetParameterBytes(false);
        if (reference.Type != actual.Type || reference.Unk04 != actual.Unk04
            || reference.StartTime != actual.StartTime || reference.EndTime != actual.EndTime
            || actualBytes.Length < referenceBytes.Length
            || !actualBytes.AsSpan(0, referenceBytes.Length).SequenceEqual(referenceBytes)
            || actualBytes.AsSpan(referenceBytes.Length).ToArray().Any(value => value != 0))
            throw new Exception($"Private animation {id} source event {i} changed: "
                + $"{reference.Type}/{reference.Unk04}/{reference.StartTime}/{reference.EndTime}/{Convert.ToHexString(referenceBytes)} "
                + $"-> {actual.Type}/{actual.Unk04}/{actual.StartTime}/{actual.EndTime}/{Convert.ToHexString(actualBytes)}");
        if ((reference.Group == null ? -1 : source.EventGroups.IndexOf(reference.Group))
            != (actual.Group == null ? -1 : animation.EventGroups.IndexOf(actual.Group)))
            throw new Exception($"Private animation {id} source event {i} changed groups");
        if (actualBytes.Length != referenceBytes.Length) paddedEvents++;
    }
}
if (!behaviorReadback.Files.Single(f => f.ID == graphMember.ID).Bytes.Span.SequenceEqual(File.ReadAllBytes(graphInput)))
    throw new Exception("Behavior graph changed during binder write");
if (Hash(animationInput) != animationHash || Hash(behaviorInput) != behaviorHash || Hash(graphInput) != graphHash)
    throw new Exception("An input changed during the build");
File.WriteAllText(Path.Combine(output, "validation.json"), JsonSerializer.Serialize(new {
    animationInput, animationHash, behaviorInput, behaviorHash, graphHash,
    animationCandidate, animationCandidateHash = Hash(animationCandidate),
    behaviorCandidate, behaviorCandidateHash = Hash(behaviorCandidate),
    tiers = expected, paddedDuplicateEvents = paddedEvents,
    preservedOriginalTimelineRecords = true, preservedOtherBinderMembers = true, gameTested = false
}, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine("Verified four private c2500 routes and preserved all other binder members.");
