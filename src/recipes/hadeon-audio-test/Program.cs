using SoulsFormats;
using Andre.Formats;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text.Json;

// Guarded candidate builder; inputs and editor workspaces are never overwritten.
if (args.Length != 4) throw new ArgumentException("regulation.bin output-directory Smithbox-directory bank-id");
var input = Path.GetFullPath(args[0]);
var output = Path.GetFullPath(args[1]);
var lib = Path.GetFullPath(args[2]);
var bankId = short.Parse(args[3]);
if (bankId < 1 || bankId > 9999) throw new ArgumentException("Character bank ID must be 1..9999");
if (Directory.Exists(output)) throw new IOException("Use a new candidate directory");
AssemblyLoadContext.Default.Resolving += (context, name) => {
    var path = Path.Combine(lib, name.Name + ".dll");
    return File.Exists(path) ? context.LoadFromAssemblyPath(path) : null;
};
Directory.SetCurrentDirectory(lib);
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)));
var inputHash = Hash(input);
var original = SFUtil.DecryptERRegulation(input);
var def = PARAMDEF.XmlDeserialize(Path.Combine(lib, "Assets/PARAM/ER/Defs/NpcParam.xml"), true);
Param Read(BND4 binder) {
    var value = Param.Read(binder.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "NpcParam").Bytes);
    value.ApplyParamdef(def, ulong.Parse(binder.Version), "NpcParam");
    return value;
}
string Rows(Param value) => JsonSerializer.Serialize(value.Rows.Select(row => new {
    row.ID, row.Name, Cells = row.Cells.ToDictionary(c => c.Def.InternalName, c => c.Value)
}));
var npc = Read(original);
var before = Rows(npc);
var row = npc.Rows.Single(r => r.ID == 25000011);
var cell = row.Cells.Single(c => c.Def.InternalName == "SoundAddBankId");
if (Convert.ToInt32(cell.Value) != -1) throw new Exception("Hadeon already has an additional bank; review before changing it");
if (Convert.ToInt32(row.Cells.Single(c => c.Def.InternalName == "SoundBankId").Value) != -1)
    throw new Exception("Original model sound bank changed; review baseline");
var oldValue = cell.Value;
cell.Value = Convert.ChangeType(bankId, oldValue.GetType());
var expected = Rows(npc);
original.Files.Single(f => Path.GetFileNameWithoutExtension(f.Name) == "NpcParam").Bytes = npc.Write();
Directory.CreateDirectory(output);
var candidate = Path.Combine(output, "regulation.bin");
SFUtil.EncryptERRegulation(candidate, original, original.Compression);
var actual = SFUtil.DecryptERRegulation(candidate);
var baseline = SFUtil.DecryptERRegulation(input);
if (actual.Files.Count != baseline.Files.Count || actual.Version != baseline.Version || actual.Compression != baseline.Compression
    || actual.Format != baseline.Format || actual.BigEndian != baseline.BigEndian || actual.BitBigEndian != baseline.BitBigEndian
    || actual.Unicode != baseline.Unicode || actual.Extended != baseline.Extended || actual.Unk04 != baseline.Unk04 || actual.Unk05 != baseline.Unk05)
    throw new Exception("Binder metadata drift");
for (int i = 0; i < baseline.Files.Count; i++) {
    var a = baseline.Files[i]; var b = actual.Files[i];
    if (a.Name != b.Name || a.ID != b.ID || a.Flags != b.Flags || a.CompressionType != b.CompressionType)
        throw new Exception("Member metadata drift");
    if (Path.GetFileNameWithoutExtension(a.Name) != "NpcParam" && !a.Bytes.Span.SequenceEqual(b.Bytes.Span))
        throw new Exception("Unrelated table changed");
}
var readback = Read(actual);
if (Rows(readback) != expected) throw new Exception("Readback differs from expected NPC table");
readback.Rows.Single(r => r.ID == 25000011).Cells.Single(c => c.Def.InternalName == "SoundAddBankId").Value = oldValue;
if (Rows(readback) != before) throw new Exception("Unrelated NPC row or field changed");
if (Hash(input) != inputHash) throw new Exception("Input changed during build");
File.WriteAllText(Path.Combine(output, "validation.json"), JsonSerializer.Serialize(new {
    input, inputHash, candidate, outputHash = Hash(candidate), row = 25000011,
    field = "SoundAddBankId", before = -1, after = bankId,
    preservedOtherTablesAndMetadata = true, preservedOtherNpcFields = true, gameplayVerified = false
}, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine("Verified one NPC field; every other decoded NPC field, table and binder metadata preserved.");
