using System.Runtime.Loader;
using System.Text.Json;
using System.Text.Json.Nodes;
using SoulsFormats;

var libraryRoot = Environment.GetEnvironmentVariable("SOVEREIGN_SMITHBOX")
    ?? throw new InvalidOperationException("SOVEREIGN_SMITHBOX is required.");
AssemblyLoadContext.Default.Resolving += (context, name) => {
    var path = Path.Combine(libraryRoot, name.Name + ".dll");
    return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
};
Run(args);

static void Run(string[] args) {
    if (args.Length != 2 || args[0] != "event-json")
        throw new ArgumentException("Usage: Inspect event-json <emevd.dcx>");
    var file = EMEVD.Read(args[1]);
    var options = new JsonSerializerOptions { IncludeFields = true };
    // Serialize public event data, including instructions, parameter bindings,
    // rest behavior, linked-file offsets, string data and format metadata.
    // Compression encoding may differ without changing event semantics.
    var data = JsonSerializer.SerializeToNode(file, options)!.AsObject();
    data.Remove("Compression");
    Console.WriteLine(data.ToJsonString());
}
