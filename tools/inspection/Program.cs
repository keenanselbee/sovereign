using System.Runtime.Loader;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Security.Cryptography;
using System.IO.Compression;
using System.Buffers.Binary;
using SoulsFormats;

var libraryRoot = Environment.GetEnvironmentVariable("SOVEREIGN_SMITHBOX")
    ?? throw new InvalidOperationException("SOVEREIGN_SMITHBOX is required.");
AssemblyLoadContext.Default.Resolving += (context, name) => {
    var path = Path.Combine(libraryRoot, name.Name + ".dll");
    return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
};
Run(args);

static void Run(string[] args) {
    var options = new JsonSerializerOptions { IncludeFields = true };
    if (args.Length == 6 && args[0] == "merge-esd-groups") {
        // Compile both DSL versions, then transplant only explicitly owned groups.
        // Original expressions, metadata and unrelated dialogue remain in the template.
        var template = BND4.Read(args[1]);
        var baseline = BND4.Read(args[2]);
        var edited = BND4.Read(args[3]);
        var manifest = JsonNode.Parse(File.ReadAllText(args[4]))!;
        var member = manifest["member"]!.GetValue<string>();
        var allowed = manifest["groups"]!.AsArray().Select(n => n!.GetValue<long>()).ToHashSet();
        if (allowed.Count == 0 || Path.GetFileName(member) != member || !member.EndsWith(".esd"))
            throw new ArgumentException("Expected one ESD member and explicit state groups");
        BinderFile Find(BND4 b) => b.Files.Single(f => f.Name.Replace('\\', '/').Split('/').Last() == member);
        var target = Find(template);
        var old = ESD.Read(Find(baseline).Bytes);
        var next = ESD.Read(Find(edited).Bytes);
        var current = ESD.Read(target.Bytes);
        string Encode(object value) => JsonSerializer.Serialize(value, options);
        var changed = old.StateGroups.Keys.Union(next.StateGroups.Keys).Where(id =>
            !old.StateGroups.ContainsKey(id) || !next.StateGroups.ContainsKey(id)
            || Encode(old.StateGroups[id]) != Encode(next.StateGroups[id])).ToHashSet();
        if (!changed.IsSubsetOf(allowed))
            throw new InvalidOperationException("DSL changes exceed the reviewed ESD group scope");
        var folder = Path.GetDirectoryName(Path.GetFullPath(args[4]))!;
        var originalName = manifest["original"]!.GetValue<string>();
        if (Path.GetFileName(originalName) != originalName)
            throw new ArgumentException("Original ESD must be a direct manifest companion");
        var originalBytes = File.ReadAllBytes(Path.Combine(folder, originalName));
        var hash = Convert.ToHexString(SHA256.HashData(originalBytes)).ToLowerInvariant();
        if (hash != manifest["originalHash"]!.GetValue<string>())
            throw new InvalidOperationException("Original ESD fingerprint changed");
        var original = ESD.Read(originalBytes);
        // Refuse to discard an unreviewed change already present in the supplied template.
        var currentMeta = JsonSerializer.SerializeToNode(current, options)!.AsObject();
        var originalMeta = JsonSerializer.SerializeToNode(original, options)!.AsObject();
        currentMeta.Remove("StateGroups"); originalMeta.Remove("StateGroups");
        if (!JsonNode.DeepEquals(currentMeta, originalMeta))
            throw new InvalidOperationException("Template ESD metadata differs from the preserved original");
        foreach (var id in current.StateGroups.Keys.Union(original.StateGroups.Keys).Except(allowed)) {
            if (!current.StateGroups.ContainsKey(id) || !original.StateGroups.ContainsKey(id)
                || Encode(current.StateGroups[id]) != Encode(original.StateGroups[id]))
                throw new InvalidOperationException("Unowned template state group changed: " + id);
        }
        foreach (var id in changed) {
            if (next.StateGroups.TryGetValue(id, out var states)) original.StateGroups[id] = states;
            else original.StateGroups.Remove(id);
        }
        target.Bytes = original.Write();
        if (!JsonNode.DeepEquals(JsonSerializer.SerializeToNode(ESD.Read(target.Bytes), options),
                                JsonSerializer.SerializeToNode(original, options)))
            throw new InvalidOperationException("ESD writer changed decoded values");
        if (File.Exists(args[5])) throw new IOException("Output already exists");
        template.Write(args[5]);
        Console.WriteLine(JsonSerializer.Serialize(new { member, changedGroups = changed.Order().ToArray() }));
        return;
    }
    if (args.Length >= 4 && args[0] == "extract-esds") {
        var binder = BND4.Read(args[1]);
        var directory = Path.GetFullPath(args[2]);
        Directory.CreateDirectory(directory);
        foreach (var name in args.Skip(3)) {
            if (Path.GetFileName(name) != name || !name.EndsWith(".esd", StringComparison.Ordinal))
                throw new ArgumentException("Expected a direct ESD member basename");
            var matches = binder.Files.Where(f => f.Name.Replace('\\', '/').Split('/').Last() == name).ToList();
            if (matches.Count != 1) throw new InvalidOperationException("ESD member must match uniquely: " + name);
            using var output = new FileStream(Path.Combine(directory, name), FileMode.CreateNew);
            output.Write(matches[0].Bytes.Span);
        }
        return;
    }
    if (args.Length == 3 && args[0] == "edit-fmgs") {
        // The caller supplies an isolated unpacked folder and a reviewed exact-value patch.
        var root = Path.GetFullPath(args[1]);
        var patch = JsonNode.Parse(File.ReadAllText(args[2]))!.AsArray();
        var loaded = new Dictionary<string, FMG>();
        var seen = new HashSet<string>();
        foreach (var entry in patch) {
            string name = entry!["file"]!.GetValue<string>();
            if (Path.GetFileName(name) != name || !name.EndsWith(".fmg", StringComparison.Ordinal))
                throw new ArgumentException("Patch must name a direct binary FMG child");
            int id = entry["id"]!.GetValue<int>();
            if (!seen.Add(name + ":" + id)) throw new ArgumentException("Duplicate FMG patch ID");
            if (!entry.AsObject().ContainsKey("before") || !entry.AsObject().ContainsKey("after"))
                throw new ArgumentException("Each patch requires before and after, including explicit nulls");
            if (!loaded.TryGetValue(name, out var fmg)) loaded[name] = fmg = FMG.Read(Path.Combine(root, name));
            var rows = fmg.Entries.Where(e => e.ID == id).ToList();
            if (entry["beforeMissing"]?.GetValue<bool>() == true) {
                if (rows.Count != 0 || entry["before"] != null)
                    throw new InvalidOperationException("New FMG entry must be absent, not existing null");
                var index = fmg.Entries.FindIndex(e => e.ID > id);
                fmg.Entries.Insert(index < 0 ? fmg.Entries.Count : index,
                    new FMG.Entry(fmg, id, entry["after"]?.GetValue<string>()));
                continue;
            }
            if (rows.Count != 1 || rows[0].Text != entry["before"]?.GetValue<string>())
                throw new InvalidOperationException($"Expected old text does not match uniquely: {name}:{id}");
            rows[0].Text = entry["after"]?.GetValue<string>();
        }
        foreach (var (name, fmg) in loaded) fmg.Write(Path.Combine(root, name));
        return;
    }
    if (args.Length == 2 && args[0] is "binder-json" or "text-json" or "dialogue-json") {
        BND4 binder;
        object compression;
        try {
            binder = BND4.Read(args[1]);
            compression = binder.Compression;
        } catch (FormatException) {
            // Qualified read-only support for this mod's historical Witchy DFLT envelope.
            var bytes = File.ReadAllBytes(args[1]);
            if (bytes.Length < 78 || !DCX.Is(bytes) || System.Text.Encoding.ASCII.GetString(bytes, 40, 4) != "DFLT"
                || BinaryPrimitives.ReadInt32BigEndian(bytes.AsSpan(16, 4)) != 68
                || BinaryPrimitives.ReadInt32BigEndian(bytes.AsSpan(32, 4)) != bytes.Length - 76) throw;
            int expected = BinaryPrimitives.ReadInt32BigEndian(bytes.AsSpan(28, 4));
            using var stream = new ZLibStream(new MemoryStream(bytes, 76, bytes.Length - 76), CompressionMode.Decompress);
            using var output = new MemoryStream();
            stream.CopyTo(output);
            if (output.Length != expected) throw new FormatException("Invalid DFLT decoded length");
            binder = BND4.Read(output.ToArray());
            compression = "Witchy DFLT " + Convert.ToHexString(bytes.AsSpan(0, 28)) + Convert.ToHexString(bytes.AsSpan(36, 40));
        }
        var entries = binder.Files.Select(f => new {
            f.ID, f.Name, f.Flags, f.CompressionType,
            Payload = args[0] == "text-json"
                ? JsonSerializer.SerializeToNode(FMG.Read(f.Bytes), options)
                : args[0] == "dialogue-json"
                ? JsonSerializer.SerializeToNode(ESD.Read(f.Bytes), options)
                : JsonSerializer.SerializeToNode(new { Size = f.Bytes.Length,
                    Sha256 = Convert.ToHexString(SHA256.HashData(f.Bytes.Span)).ToLowerInvariant() }, options)
        }).ToList();
        Console.WriteLine(JsonSerializer.Serialize(new { binder.Version, binder.Format, binder.BigEndian,
            binder.BitBigEndian, binder.Unicode, binder.Extended, binder.Unk04, binder.Unk05,
            Compression = compression, Files = entries }, options));
        return;
    }
    if (args.Length != 2 || args[0] != "event-json")
        throw new ArgumentException("Usage: Inspect event-json|binder-json|text-json|dialogue-json <file>; edit-fmgs <directory> <patch.json>");
    var file = EMEVD.Read(args[1]);
    // Serialize public event data, including instructions, parameter bindings,
    // rest behavior, linked-file offsets, string data and format metadata.
    // Compression encoding may differ without changing event semantics.
    var data = JsonSerializer.SerializeToNode(file, options)!.AsObject();
    data.Remove("Compression");
    Console.WriteLine(data.ToJsonString());
}
