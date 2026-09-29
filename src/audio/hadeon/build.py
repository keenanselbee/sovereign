"""Pack and independently validate Hadeon's segmented sixteen-line Wwise bank."""

import argparse
import json
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path

from prepare import BANK_DIR, MANIFEST, ROOT, SCRATCH, SOURCE, digest, pcm_description, riff_chunk


REWWISE = Path(r"Z:\Modding\Elden Ring\Tools\Sound\bnk2json.exe")
REWWISE_SHA256 = "B175F116A4D301C1C44C07B0EB221E6A50F126574F8A09CB8CEDDE748DC88505"
BANK_ID = 1155255848
MIXER_VOICE_GAIN_DB = 2.0


def chunks(path):
    with path.open("rb") as stream:
        while header := stream.read(8):
            if len(header) != 8:
                raise ValueError(f"Truncated chunk header in {path}")
            kind, size = struct.unpack("<4sI", header)
            data = stream.read(size)
            if len(data) != size:
                raise ValueError(f"Truncated {kind!r} chunk in {path}")
            yield kind, data


def fnv(name):
    value = 2166136261
    for byte in name.lower().encode("utf-8"):
        value = ((value * 16777619) ^ byte) & 0xFFFFFFFF
    return value


def section(document, name):
    return next(item["body"][name] for item in document["sections"] if name in item["body"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, default=SCRATCH,
                        help="Preparation directory containing prepared.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    if not scratch.is_relative_to((ROOT / ".codex-temp").resolve()):
        parser.error("Scratch must stay beneath the repository .codex-temp directory")
    output = (args.output or scratch / "output").resolve()
    if not output.is_relative_to(scratch):
        parser.error(f"Output must stay inside {scratch}")
    output.mkdir(parents=True, exist_ok=False)
    if digest(REWWISE) != REWWISE_SHA256:
        raise ValueError("Pinned rewwise executable changed")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    prepared = json.loads((scratch / "prepared.json").read_text(encoding="utf-8"))
    lines = manifest["lines"]
    graph = json.loads((BANK_DIR / "soundbank.json").read_text(encoding="utf-8"))
    bkhd, hirc = section(graph, "BKHD"), section(graph, "HIRC")
    if bkhd["version"] != 135 or bkhd["bank_id"] != BANK_ID or manifest["bankId"] != BANK_ID:
        raise ValueError("Native BKHD version/bank ID changed")
    objects = hirc["objects"]
    if hirc["object_count"] != len(objects) or len(objects) != prepared["objects"]:
        raise ValueError("HIRC object count mismatch")
    positions = {item["id"]["Hash"]: at for at, item in enumerate(objects) if "Hash" in item["id"]}
    if len(positions) != sum("Hash" in item["id"] for item in objects):
        raise ValueError("Duplicate HIRC object ID")
    events = {item["id"]["String"]: item["body"]["Event"]["actions"] for item in objects
              if "Event" in item["body"]}
    if len(events) != prepared["events"]:
        raise ValueError("Duplicate/missing event name")
    for at, item in enumerate(objects):
        body = next(iter(item["body"].values()))
        for child in body.get("children", {}).get("items", []):
            if positions.get(child, at) >= at:
                raise ValueError("Child sound is not before parent")
        for action in body.get("actions", []):
            if positions.get(action, at) >= at:
                raise ValueError("Action is not before event")
        if "Action" in item["body"] and positions.get(body["external_id"], at) >= at:
            raise ValueError("Sound is not before its action")
    by_id = {item["id"]["Hash"]: next(iter(item["body"].values()))
             for item in objects if "Hash" in item["id"]}
    mixer = by_id[3900000000]
    if mixer["node_base_params"]["override_bus_id"] != 3170124113:
        raise ValueError("Native voice bus changed")
    positioning = mixer["node_base_params"]["positioning_params"]
    if not (positioning["override_parent"] and positioning["enable_attenuation"] and
            positioning["listener_relative_routing"] and
            positioning["three_dimensional_spatialization_mode"] == "PositionAndOrientation"):
        raise ValueError("Original listener-relative attenuation changed")
    if mixer["node_base_params"]["node_initial_params"]["prop_initial_values"] != [
        {"Volume": MIXER_VOICE_GAIN_DB}, {"Priority": 80.0}, {"CenterPCT": 50.0},
        {"GameAuxSendVolume": -12.0},
        {"AttenuationID": 3900000004}]:
        raise ValueError("Hadeon mixer voice properties changed")

    media_files = {}
    expected_children = [3900000001, *range(3900000010, 3900000015), 3900001100]

    def check_sound(node, media_id):
        body = by_id[node]
        source = body["bank_source_data"]
        wem = BANK_DIR / f"{media_id}.wem"
        if body["node_base_params"]["direct_parent_id"] != 3900000000 or \
                body["node_base_params"]["node_initial_params"]["prop_initial_values"] != [] or \
                source["plugin"] != "PCM" or source["source_type"] != "Embedded" or \
                source["media_information"] != {"source_id": media_id,
                    "in_memory_media_size": wem.stat().st_size, "source_flags": 0}:
            raise ValueError(f"Unexpected sound object/media declaration: {media_id}")
        if pcm_description(wem)[:4] != (0xFFFE, 1, 48000, 16):
            raise ValueError(f"Unexpected WEM PCM format: {media_id}")
        if digest(wem) != prepared["wemHashes"][str(media_id)]:
            raise ValueError(f"WEM changed since conversion: {media_id}")
        media_files[media_id] = wem

    def check_action(action, node, is_play):
        body = by_id[action]
        if body["external_id"] != node or body["action_type"] != (1027 if is_play else 259):
            raise ValueError(f"Unexpected voice action {action}")
        if is_play and body["params"]["Play"]["bank_id"] != BANK_ID:
            raise ValueError(f"Unexpected play bank ID {action}")
        if not is_play and body["params"] != by_id[3900000003]["params"]:
            raise ValueError(f"Unexpected stop behavior {action}")

    for line in lines:
        index = line["index"]
        original = SOURCE / "recordings" / line["recording"]
        converted = SOURCE / "converted" / line["recording"].replace(".wav", "-48k.wav")
        if digest(original) != prepared["sourceHashes"][str(index)] or \
                digest(converted) != prepared["convertedHashes"][str(index)]:
            raise ValueError(f"Source or conversion changed: {line['key']}")
        expected_samples = (prepared["segmentSamples"][str(line["soundId"])] if index == 0
                            else pcm_description(converted)[-1])
        if expected_samples != pcm_description(BANK_DIR / f"{line['soundId']}.wem")[-1]:
            raise ValueError(f"Full voice duration changed: {line['key']}")
        node = 3900000001 if index == 0 else 3900001000 + index
        if index:
            expected_children.append(node)
        check_sound(node, line["soundId"])
        play = 3900000002 if index == 0 else 3900003000 + index
        stop = 3900000003 if index == 0 else 3900003100 + index
        check_action(play, node, True)
        check_action(stop, node, False)
        if events[f"Play_v{line['soundId']}"] != [play] or \
                events[f"Stop_v{line['soundId']}"] != [stop] or \
                events[f"Play_v{line['stopAlias']}"] != [stop]:
            raise ValueError(f"Full voice play/stop event mismatch: {line['key']}")
        for cue_index, cue in enumerate(line["cues"]):
            carrier = line["carrierBase"] + cue_index
            cue_node = 3900000010 + cue_index if index == 0 else 3900002000 + index * 10 + cue_index
            if index:
                expected_children.append(cue_node)
            check_sound(cue_node, carrier)
            cue_play = 3900000020 + cue_index if index == 0 else 3900004000 + index * 10 + cue_index
            cue_stop = 3900000030 + cue_index if index == 0 else 3900005000 + index * 10 + cue_index
            check_action(cue_play, cue_node, True)
            check_action(cue_stop, cue_node, False)
            if events[f"Play_v{carrier}"] != [cue_play] or events[f"Stop_v{carrier}"] != [cue_stop]:
                raise ValueError(f"Subtitle carrier event mismatch: {carrier}")
            wave_path = (SOURCE / "subtitle-cues" /
                         (f"subtitle-cue-{cue_index + 1:02}.wav" if index == 0 else
                          f"subtitle-cue-{index:02}-{cue_index:02}.wav"))
            if pcm_description(wave_path) != (1, 1, 48000, 16, prepared["cueSamples"][str(carrier)]) or \
                    pcm_description(BANK_DIR / f"{carrier}.wem")[-1] != prepared["cueSamples"][str(carrier)] or \
                    any(riff_chunk(wave_path, b"data")) or any(riff_chunk(BANK_DIR / f"{carrier}.wem", b"data")):
                raise ValueError(f"Carrier is not exact silent PCM: {carrier}")
    final = lines[0]["finalSegment"]
    first_segment = SOURCE / "converted/hadeon-entrance-first-through-hither-48k.wav"
    final_segment = SOURCE / "converted/hadeon-entrance-first-to-my-blade-48k.wav"
    if final["start"] != lines[0]["cues"][-1]["start"] or \
            final["soundId"] != 999800003 or final["stopAlias"] != 999800004:
        raise ValueError("First entrance segment timing or IDs changed")
    full_pcm = riff_chunk(SOURCE / "converted/hadeon-entrance-first-48k.wav", b"data")
    if riff_chunk(first_segment, b"data") + riff_chunk(final_segment, b"data") != full_pcm:
        raise ValueError("First entrance segments do not reproduce the source PCM")
    for media_id, path in ((lines[0]["soundId"], first_segment), (final["soundId"], final_segment)):
        if digest(path) != prepared["segmentHashes"][str(media_id)] or \
                pcm_description(path)[-1] != prepared["segmentSamples"][str(media_id)]:
            raise ValueError(f"First entrance segment changed: {path}")
    check_sound(3900001100, final["soundId"])
    check_action(3900003200, 3900001100, True)
    check_action(3900003210, 3900001100, False)
    if events[f"Play_v{final['soundId']}"] != [3900003200] or \
            events[f"Stop_v{final['soundId']}"] != [3900003210] or \
            events[f"Play_v{final['stopAlias']}"] != [3900003210]:
        raise ValueError("Final phrase play/stop event mismatch")
    if mixer["children"]["items"] != expected_children or len(media_files) != prepared["mediaCount"]:
        raise ValueError("Mixer child order/media count mismatch")

    with tempfile.TemporaryDirectory(prefix="hadeon-bank-", dir=output) as temp:
        staged = Path(temp) / "cs_c9998"
        shutil.copytree(BANK_DIR, staged)
        result = subprocess.run([str(REWWISE), str(staged)], capture_output=True, text=True)
        (output / "pack.log").write_text(result.stdout + result.stderr, encoding="utf-8")
        created = Path(temp) / "cs_c9998.created.bnk"
        if result.returncode or not created.is_file():
            raise RuntimeError(f"Bank packing failed: {result.returncode}")
        bank = output / "cs_c9998.bnk"
        shutil.copyfile(created, bank)
    parts = dict(chunks(bank))
    if struct.unpack_from("<II", parts[b"BKHD"])[0:2] != (135, BANK_ID):
        raise ValueError("Packed bank BKHD mismatch")
    if len(parts[b"DIDX"]) != 12 * len(media_files) or struct.unpack_from("<I", parts[b"HIRC"])[0] != len(objects):
        raise ValueError("Packed bank DIDX/HIRC count mismatch")
    embedded = set()
    for offset in range(0, len(parts[b"DIDX"]), 12):
        media_id, data_offset, size = struct.unpack_from("<III", parts[b"DIDX"], offset)
        if media_id in embedded or media_id not in media_files or data_offset % 16 != 0 or \
                parts[b"DATA"][data_offset:data_offset + size] != media_files[media_id].read_bytes():
            raise ValueError(f"Packed media mismatch: {media_id}")
        embedded.add(media_id)
    if embedded != set(media_files):
        raise ValueError("Packed media incomplete")

    # A separate rewwise decode catches graph serialization and media extraction drift.
    result = subprocess.run([str(REWWISE), str(bank)], capture_output=True, text=True)
    (output / "readback.log").write_text(result.stdout + result.stderr, encoding="utf-8")
    readback = output / "cs_c9998"
    if result.returncode or not (readback / "soundbank.json").is_file():
        raise RuntimeError(f"Bank readback failed: {result.returncode}")
    decoded = json.loads((readback / "soundbank.json").read_text(encoding="utf-8"))
    expected = json.loads(json.dumps(objects))
    for item in expected:
        if "String" in item["id"]:
            item["id"] = {"Hash": fnv(item["id"]["String"])}
    if section(decoded, "HIRC")["objects"] != expected:
        raise ValueError("Independent HIRC readback differs")
    for media_id, wem in media_files.items():
        if (readback / wem.name).read_bytes() != wem.read_bytes():
            raise ValueError(f"Independent WEM readback differs: {media_id}")
    report = {"bank": str(bank), "sha256": digest(bank), "bytes": bank.stat().st_size,
              "bkhdVersion": 135, "hircObjects": len(objects), "events": len(events),
              "media": len(media_files), "mixerVoiceGainDb": MIXER_VOICE_GAIN_DB,
              "sourceAndWemHashesStable": True,
              "graphAndMediaReadbackEqual": True,
              "voiceDurations": prepared["durations"]}
    (output / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
