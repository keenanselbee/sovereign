using SoulsFormats;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text.Json;

if (args.Length != 5)
    throw new ArgumentException("c2500.anibnd.dcx c2500.behbnd.dcx candidate-graph.hkx output-directory Smithbox-directory");
var animationInput = Path.GetFullPath(args[0]);
var behaviorInput = Path.GetFullPath(args[1]);
var graphInput = Path.GetFullPath(args[2]);
var output = Path.GetFullPath(args[3]);
var library = Path.GetFullPath(args[4]);
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
AssemblyLoadContext.Default.Resolving += (context, name) => {
    var path = Path.Combine(library, name.Name + ".dll");
    return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(library);
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)));
var animationHash = Hash(animationInput);
var behaviorHash = Hash(behaviorInput);
var graphHash = Hash(graphInput);
var animationBinder = BND4.Read(animationInput);
var timeline = TAE.Read(animationBinder.Files.Single(file => file.Name.EndsWith(".tae")).Bytes);
if (timeline.Animations.Count != 282)
    throw new InvalidOperationException("Accepted animation count changed");
for (var id = 3030; id <= 3033; id++) {
    var animation = timeline.Animations.Single(a => a.ID == id);
    var header = animation.MiniHeader as TAE.Animation.AnimMiniHeader.Standard;
    if (header == null || !header.ImportsHKX || header.ImportHKXSourceAnimID != 3028
        || animation.Events.Count != 65
        || animation.Events.Count(e => e.Type == 67 && BitConverter.ToInt32(e.GetParameterBytes(false), 0) is 1627600 or 1627601) != 2)
        throw new InvalidOperationException($"Private timeline {id} changed");
}
var binder = BND4.Read(behaviorInput);
var graph = binder.Files.Single(file => file.ID == 7000501 && file.Name.EndsWith("c9997.hkx"));
if (graph.Bytes.Span.SequenceEqual(File.ReadAllBytes(graphInput)))
    throw new InvalidOperationException("The candidate graph is unchanged");
graph.Bytes = File.ReadAllBytes(graphInput);
Directory.CreateDirectory(output);
var candidate = Path.Combine(output, "c2500.behbnd.dcx");
binder.Write(candidate);
var readback = BND4.Read(candidate);
var baseline = BND4.Read(behaviorInput);
if (baseline.Files.Count != readback.Files.Count || baseline.Version != readback.Version
    || baseline.Compression != readback.Compression || baseline.Format != readback.Format
    || baseline.BigEndian != readback.BigEndian || baseline.BitBigEndian != readback.BitBigEndian
    || baseline.Unicode != readback.Unicode || baseline.Extended != readback.Extended)
    throw new InvalidOperationException("Binder metadata drift");
for (var index = 0; index < baseline.Files.Count; index++) {
    var before = baseline.Files[index];
    var after = readback.Files[index];
    if (before.Name != after.Name || before.ID != after.ID || before.Flags != after.Flags
        || before.CompressionType != after.CompressionType)
        throw new InvalidOperationException("Binder member metadata drift");
    if (before.ID != graph.ID && !before.Bytes.Span.SequenceEqual(after.Bytes.Span))
        throw new InvalidOperationException($"Unrelated binder member changed: {before.Name}");
}
if (!readback.Files.Single(file => file.ID == graph.ID).Bytes.Span.SequenceEqual(File.ReadAllBytes(graphInput)))
    throw new InvalidOperationException("Graph changed during binder write");
if (Hash(animationInput) != animationHash || Hash(behaviorInput) != behaviorHash || Hash(graphInput) != graphHash)
    throw new InvalidOperationException("An input changed during the build");
File.WriteAllText(Path.Combine(output, "validation.json"), JsonSerializer.Serialize(new {
    animationInput, animationHash, behaviorInput, behaviorHash, graphHash,
    candidate, candidateHash = Hash(candidate), preservedAnimationBinder = true,
    preservedOtherBehaviorMembers = true, gameTested = false
}, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine("Verified four private timelines and the graph-only behavior binder candidate.");
