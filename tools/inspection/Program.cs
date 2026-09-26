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
    if (args.Length == 4 && args[0] == "tracked-members") {
        var input = Path.GetFullPath(args[1]);
        var destination = Path.GetFullPath(args[3]);
        if (Directory.Exists(destination) || File.Exists(destination))
            throw new IOException("Tracked output directory must be new: " + destination);
        var archive = JsonNode.Parse(File.ReadAllText(args[2]))?.AsObject()
            ?? throw new ArgumentException("Expected one archive object");
        var runtime = archive["runtime"]?.GetValue<string>()
            ?? throw new ArgumentException("Archive spec lacks runtime");
        if (Path.GetFileName(input) != runtime.Replace('\\', '/').Split('/').Last())
            throw new ArgumentException("Runtime binary does not match archive spec: " + runtime);
        var inputHash = HashFile(input);
        var files = new JsonArray();
        var pending = new List<byte[]>();
        void Record(JsonObject item, byte[] bytes) {
            var source = item["source"]?.GetValue<string>();
            if (string.IsNullOrWhiteSpace(source)) throw new ArgumentException("Tracked source path is required");
            var name = pending.Count.ToString("D6");
            var hash = Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
            item["sha256"] = hash;
            item["size"] = bytes.Length;
            files.Add(new JsonObject { ["source"] = source, ["candidate"] = name,
                ["sha256"] = hash, ["size"] = bytes.Length });
            pending.Add(bytes);
        }
        if (archive["members"] is JsonArray members) {
            var (binder, compression) = ReadBinder(input);
            var available = binder.Files.ToList();
            var used = new HashSet<BinderFile>();
            var untrackedTextures = new JsonArray();
            foreach (var entry in members) {
                var member = entry?.AsObject() ?? throw new ArgumentException("Invalid tracked member");
                var name = member["archiveName"]?.GetValue<string>()
                    ?? throw new ArgumentException("Tracked member lacks archiveName");
                var matches = available.Where(f => f.Name == name).ToList();
                if (matches.Count > 1 && member["id"] != null)
                    matches = matches.Where(f => f.ID == member["id"]!.GetValue<int>()).ToList();
                if (matches.Count != 1 || !used.Add(matches[0]))
                    throw new InvalidOperationException("Tracked member is absent or ambiguous: " + name);
                var matchedFile = matches[0];
                member["id"] = matchedFile.ID;
                member["flags"] = matchedFile.Flags.ToString();
                member["compression"] = matchedFile.CompressionType.ToString();
                var bytes = matchedFile.Bytes.ToArray();
                Record(member, bytes);
                if (member["textures"] is not JsonArray textures || textures.Count == 0) continue;
                var tpf = TPF.Read(bytes);
                var availableTextures = tpf.Textures.ToList();
                var usedTextures = new HashSet<string>(StringComparer.Ordinal);
                foreach (var textureEntry in textures) {
                    var texture = textureEntry?.AsObject() ?? throw new ArgumentException("Invalid tracked texture");
                    var textureName = texture["name"]?.GetValue<string>()
                        ?? throw new ArgumentException("Tracked texture lacks name");
                    var textureMatches = availableTextures.Where(t => t.Name == textureName).ToList();
                    if (textureMatches.Count != 1 || !usedTextures.Add(textureName))
                        throw new InvalidOperationException("Tracked texture is absent or ambiguous: " + textureName);
                    var found = textureMatches[0];
                    texture["format"] = found.Format;
                    texture["type"] = found.Type.ToString();
                    texture["mipmaps"] = found.Mipmaps;
                    texture["flags"] = found.Flags1;
                    Record(texture, found.Bytes);
                }
                foreach (var extra in availableTextures.Where(t => !usedTextures.Contains(t.Name)))
                    untrackedTextures.Add(new JsonObject { ["member"] = name, ["name"] = extra.Name });
            }
            var untracked = available.Where(f => !used.Contains(f)).ToList();
            if (archive["completeMemberSet"]?.GetValue<bool>() == true && untracked.Count != 0)
                throw new InvalidOperationException("Complete tracked member set changed: " + untracked.Count + " untracked members");
            archive["sha256"] = inputHash;
            archive["totalMembers"] = available.Count;
            archive["header"] = JsonSerializer.SerializeToNode(new { binder.Version, Format = binder.Format.ToString(),
                binder.BigEndian, binder.BitBigEndian, binder.Unicode, binder.Extended,
                binder.Unk04, binder.Unk05, Compression = compression.ToString() }, options);
            archive["untrackedMembers"] = new JsonArray(untracked.Select(f => (JsonNode?)new JsonObject {
                ["archiveName"] = f.Name, ["id"] = f.ID }).ToArray());
            archive["untrackedTextures"] = untrackedTextures;
        } else if (archive["outputs"] is JsonArray outputs) {
            if (outputs.Count != 1) throw new ArgumentException("Direct archive spec needs exactly one output");
            Record(outputs[0]?.AsObject() ?? throw new ArgumentException("Invalid direct output"), File.ReadAllBytes(input));
            archive["sha256"] = inputHash;
        } else {
            throw new ArgumentException("Archive spec needs members or outputs");
        }
        if (HashFile(input) != inputHash) throw new IOException("Runtime binary changed during tracked extraction");
        Directory.CreateDirectory(destination);
        for (var i = 0; i < pending.Count; i++)
            File.WriteAllBytes(Path.Combine(destination, i.ToString("D6")), pending[i]);
        if (HashFile(input) != inputHash) throw new IOException("Runtime binary changed during tracked extraction");
        Console.WriteLine(new JsonObject { ["archive"] = archive, ["files"] = files }.ToJsonString());
        return;
    }
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
        var (binder, compression) = ReadBinder(args[1]);
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
        throw new ArgumentException("Usage: Inspect event-json|binder-json|text-json|dialogue-json <file>; edit-fmgs <directory> <patch.json>; tracked-members <runtime-binary> <archive-spec-json> <new-output-dir>");
    var file = EMEVD.Read(args[1]);
    // Serialize public event data, including instructions, parameter bindings,
    // rest behavior, linked-file offsets, string data and format metadata.
    // Compression encoding may differ without changing event semantics.
    var data = JsonSerializer.SerializeToNode(file, options)!.AsObject();
    data.Remove("Compression");
    Console.WriteLine(data.ToJsonString());
}

static string HashFile(string path) {
    using var stream = File.OpenRead(path);
    return Convert.ToHexString(SHA256.HashData(stream)).ToLowerInvariant();
}

static (BND4 Binder, object Compression) ReadBinder(string path) {
    try {
        var binder = BND4.Read(path);
        return (binder, binder.Compression);
    } catch (FormatException) {
        // Qualified read-only support for this mod's historical Witchy DFLT envelope.
        var bytes = File.ReadAllBytes(path);
        if (bytes.Length < 78 || !DCX.Is(bytes) || System.Text.Encoding.ASCII.GetString(bytes, 40, 4) != "DFLT"
            || BinaryPrimitives.ReadInt32BigEndian(bytes.AsSpan(16, 4)) != 68
            || BinaryPrimitives.ReadInt32BigEndian(bytes.AsSpan(32, 4)) != bytes.Length - 76) throw;
        int expected = BinaryPrimitives.ReadInt32BigEndian(bytes.AsSpan(28, 4));
        using var stream = new ZLibStream(new MemoryStream(bytes, 76, bytes.Length - 76), CompressionMode.Decompress);
        using var output = new MemoryStream();
        stream.CopyTo(output);
        if (output.Length != expected) throw new FormatException("Invalid DFLT decoded length");
        var binder = BND4.Read(output.ToArray());
        return (binder, "Witchy DFLT " + Convert.ToHexString(bytes.AsSpan(0, 28)) + Convert.ToHexString(bytes.AsSpan(36, 40)));
    }
}
