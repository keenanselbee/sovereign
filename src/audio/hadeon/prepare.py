"""Derive Hadeon's wet PCM voices, silent subtitle media, and Wwise bank source."""

import argparse
import array
import copy
import hashlib
import json
import math
import shutil
import struct
import subprocess
import wave
from pathlib import Path
from xml.etree import ElementTree


SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parents[2]
MANIFEST = SOURCE / "dialogue-manifest.json"
BANK_DIR = SOURCE / "cs_c9998"
SCRATCH = ROOT / ".codex-temp/hadeon-monologue-audio/revision5"
FFMPEG = Path(r"Z:\Modding\Elden Ring\Tools\Sound\ffmpeg.exe")
WWISE = Path(r"C:\Program Files (x86)\Audiokinetic\Wwise2023.1.10.8659\Authoring\x64\Release\bin\WwiseConsole.exe")
FFMPEG_SHA256 = "4F5FB025EF287BE08E71585B41F5C3E09A04405CDFD798377A693F38E687A964"
WWISE_SHA256 = "446F9E8332F61BF01AD6C3BAA82764052AABE936BF154A95202B337509F12D1C"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def riff_chunk(path, target):
    raw = path.read_bytes()
    if raw[:4] != b"RIFF" or raw[8:12] != b"WAVE":
        raise ValueError(f"Not a RIFF WAV: {path}")
    offset = 12
    while offset + 8 <= len(raw):
        kind, size = struct.unpack_from("<4sI", raw, offset)
        offset += 8
        if kind == target:
            return raw[offset:offset + size]
        offset += size + (size & 1)
    raise ValueError(f"Missing {target!r}: {path}")


def pcm_description(path):
    fmt = riff_chunk(path, b"fmt ")
    kind, channels, rate, _, _, bits = struct.unpack_from("<HHIIHH", fmt)
    data = riff_chunk(path, b"data")
    samples = len(data) // (bits // 8 * channels)
    return kind, channels, rate, bits, samples


def run(command, *, cwd=None, log=None):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, errors="replace")
    if log is not None:
        log.write_text(result.stdout + result.stderr, encoding="utf-8")
    return result


def object_by_hash(objects, hash_id):
    return next(item for item in objects if item["id"].get("Hash") == hash_id)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, default=SCRATCH)
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    if not scratch.is_relative_to((ROOT / ".codex-temp").resolve()):
        parser.error("Scratch must stay beneath the repository .codex-temp directory")
    scratch.mkdir(parents=True, exist_ok=True)
    if digest(FFMPEG) != FFMPEG_SHA256 or digest(WWISE) != WWISE_SHA256:
        raise ValueError("Installed conversion tool differs from qualified executable")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    lines = manifest["lines"]
    if [line["index"] for line in lines] != list(range(16)):
        raise ValueError("Expected exactly sixteen indexed lines")
    media_waves = {}
    durations = {}
    cue_samples = {}
    source_hashes = {}
    converted_hashes = {}
    segment_hashes = {}
    segment_samples = {}
    converted_peaks_dbfs = {}
    for line in lines:
        index = line["index"]
        original = SOURCE / "recordings" / line["recording"]
        if not original.is_file() or line["recording"].endswith("-nr.wav"):
            raise ValueError(f"Missing wet recording: {original}")
        source_hashes[index] = digest(original)
        converted = SOURCE / "converted" / line["recording"].replace(".wav", "-48k.wav")
        original_kind, original_channels, original_rate, original_bits, original_samples = pcm_description(original)
        if index == 0 and digest(original) != "31F9F586D46E38D3CE48D4E5B1B5B323DBE758FB4321536005360E372D9543DA":
            raise ValueError("First entrance source changed")
        if index == 0 and digest(SOURCE / "recordings/hadeon-entrance-first-nr.wav") != (
                "97C32E48920B28D38EE574BA62A7121CEBCF49BC90B0B5283DD5BB586ADCA8F0"):
            raise ValueError("First entrance timing reference changed")
        command = [str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y", "-i", str(original),
                   "-af", "aresample=48000,volume=-1dB", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(converted)]
        result = run(command, log=scratch / f"ffmpeg-{index:02}.log")
        if result.returncode or not converted.is_file():
            raise RuntimeError(f"ffmpeg failed for {original.name}: {result.stderr}")
        kind, channels, rate, bits, samples = pcm_description(converted)
        if (kind, channels, rate, bits) != (1, 1, 48000, 16):
            raise ValueError(f"Converted media format changed: {converted}")
        duration = samples / 48000
        if abs(duration - original_samples / original_rate) > 1 / 48000:
            raise ValueError(f"Conversion duration changed: {converted}")
        durations[index] = duration
        converted_hashes[index] = digest(converted)
        pcm = array.array("h", riff_chunk(converted, b"data"))
        peak = max(abs(value) for value in pcm)
        # Resampling/PCM rounding can move the exact -1 dB target by a few samples.
        if peak > 29250:
            raise ValueError(f"Converted voice lacks 1 dB headroom: {converted}")
        converted_peaks_dbfs[index] = 20 * math.log10(peak / 32768)
        if index == 0:
            final = line["finalSegment"]
            if final["start"] != line["cues"][-1]["start"] or final["soundId"] != 999800003 or final["stopAlias"] != 999800004:
                raise ValueError("First entrance final segment must align with its subtitle")
            split = round(final["start"] * 48000)
            if not 0 < split < samples:
                raise ValueError("Invalid first entrance split")
            pcm_bytes = riff_chunk(converted, b"data")
            segments = ((line["soundId"], "through-hither", pcm_bytes[:split * 2]),
                        (final["soundId"], "to-my-blade", pcm_bytes[split * 2:]))
            for media_id, suffix, data in segments:
                path = SOURCE / "converted" / f"hadeon-entrance-first-{suffix}-48k.wav"
                with wave.open(str(path), "wb") as target:
                    target.setnchannels(1)
                    target.setsampwidth(2)
                    target.setframerate(48000)
                    target.writeframes(data)
                if riff_chunk(path, b"data") != data:
                    raise ValueError(f"Segment PCM changed: {path}")
                media_waves[media_id] = path
                segment_hashes[media_id] = digest(path)
                segment_samples[media_id] = len(data) // 2
        else:
            media_waves[line["soundId"]] = converted

        cues = line["cues"]
        if not cues or cues[0]["start"] != 0 or len(cues) > 10:
            raise ValueError(f"Invalid cues for {line['key']}")
        for cue_index, cue in enumerate(cues):
            start = cue["start"]
            end = cues[cue_index + 1]["start"] if cue_index + 1 < len(cues) else cue["end"]
            if not (0 <= start < end <= duration):
                raise ValueError(f"Invalid cue span for {line['key']}: {start}-{end}/{duration}")
            carrier_id = line["carrierBase"] + cue_index
            path = (SOURCE / "subtitle-cues" /
                    (f"subtitle-cue-{cue_index + 1:02}.wav" if index == 0 else
                     f"subtitle-cue-{index:02}-{cue_index:02}.wav"))
            count = round((end - start) * 48000)
            with wave.open(str(path), "wb") as target:
                target.setnchannels(1)
                target.setsampwidth(2)
                target.setframerate(48000)
                target.writeframes(b"\0" * count * 2)
            if any(riff_chunk(path, b"data")):
                raise ValueError(f"Subtitle carrier is not silent: {path}")
            cue_samples[carrier_id] = pcm_description(path)[-1]
            media_waves[carrier_id] = path

    if len(media_waves) != len(set(media_waves)):
        raise ValueError("Duplicate sound/media ID")
    project = scratch / "HadeonWwise" / "HadeonWwise.wproj"
    if not project.is_file():
        if project.parent.exists():
            raise ValueError(f"Wwise requires an absent new project directory: {project.parent}")
        result = run([str(WWISE), "create-new-project", str(project), "--platform", "Windows"],
                     log=scratch / "wwise-create.log")
        if not project.is_file():
            raise RuntimeError(f"Wwise project creation failed: {result.stderr}")
    external = ElementTree.Element("ExternalSourcesList", SchemaVersion="1", Root=str(SOURCE))
    for media_id, path in media_waves.items():
        ElementTree.SubElement(external, "Source", Path=str(path.relative_to(SOURCE)).replace("/", "\\"), Conversion="PCM")
    sources = scratch / "hadeon.wsources"
    ElementTree.ElementTree(external).write(sources, encoding="unicode", xml_declaration=False)
    converted_wems = scratch / "converted-wems"
    result = run([str(WWISE), "convert-external-source", str(project), "--source-file", str(sources),
                  "--output", str(converted_wems)], log=scratch / "wwise-convert.log")
    if result.returncode not in (0, 2):
        raise RuntimeError(f"Wwise conversion failed: {result.returncode}: {result.stderr}")
    for media_id, path in media_waves.items():
        wem_source = converted_wems / "Windows" / path.relative_to(SOURCE).with_suffix(".wem")
        if not wem_source.is_file():
            raise RuntimeError(f"Wwise did not produce {wem_source}")
        wem = BANK_DIR / f"{media_id}.wem"
        if media_id != 999800010:
            shutil.copyfile(wem_source, wem)
        if pcm_description(wem)[:4] != (0xFFFE, 1, 48000, 16):
            raise ValueError(f"Not Wwise PCM: {wem}")
        if pcm_description(wem)[-1] != pcm_description(path)[-1]:
            raise ValueError(f"Wwise media duration differs: {wem}")
        if media_id == 999800010:
            if digest(wem) != "B85949AF98003E74303FF86250A95179D7528B9200430470CCBCAFB4A11DF620":
                raise ValueError("Unchanged first subtitle carrier changed")
        elif digest(wem) != digest(wem_source):
            raise ValueError(f"Wwise media copy changed: {wem}")
    for line in lines:
        if digest(SOURCE / "recordings" / line["recording"]) != source_hashes[line["index"]]:
            raise ValueError(f"Original recording changed during conversion: {line['recording']}")

    graph_path = BANK_DIR / "soundbank.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    hirc = next(section["body"]["HIRC"] for section in graph["sections"] if "HIRC" in section["body"])
    existing = hirc["objects"]
    # The old 33-object graph is the stable template. Rebuilding is idempotent.
    originals = [obj for obj in existing if obj["id"].get("Hash", 0xFFFFFFFF) < 3900000100 or
                 "String" in obj["id"] and obj["id"]["String"] in {
                     "Stop_v999800001", "Play_v999800001", "Play_v999800002",
                     *(f"{action}_v{999800010 + cue}" for cue in range(5) for action in ("Play", "Stop"))
                 }]
    if len(originals) != 33:
        raise ValueError("Existing graph is not the qualified 33-object base")
    template_sound = object_by_hash(originals, 3900000001)
    template_sound["body"]["Sound"]["bank_source_data"]["media_information"]["in_memory_media_size"] = (
        BANK_DIR / "999800001.wem").stat().st_size
    for cue_index in range(5):
        carrier = 999800010 + cue_index
        sound = object_by_hash(originals, 3900000010 + cue_index)
        sound["body"]["Sound"]["bank_source_data"]["media_information"]["in_memory_media_size"] = (
            BANK_DIR / f"{carrier}.wem").stat().st_size
    play_template = object_by_hash(originals, 3900000002)
    stop_template = object_by_hash(originals, 3900000003)
    mixer = object_by_hash(originals, 3900000000)
    original_sounds = originals[:7]
    original_actions = originals[8:20]
    original_events = originals[20:]
    if len(original_sounds) != 7 or len(original_actions) != 12 or len(original_events) != 13:
        raise ValueError("Unexpected native graph ordering")

    new_sounds, new_actions, new_events = [], [], []

    def add_sound(node_id, media_id):
        item = copy.deepcopy(template_sound)
        item["id"] = {"Hash": node_id}
        item["body"]["Sound"]["bank_source_data"]["media_information"] = {
            "source_id": media_id, "in_memory_media_size": (BANK_DIR / f"{media_id}.wem").stat().st_size,
            "source_flags": 0,
        }
        new_sounds.append(item)
        return node_id

    def add_action(action_id, node_id, is_play):
        item = copy.deepcopy(play_template if is_play else stop_template)
        item["id"] = {"Hash": action_id}
        item["body"]["Action"]["external_id"] = node_id
        new_actions.append(item)

    def add_event(name, action_id):
        new_events.append({"id": {"String": name}, "body": {"Event": {"actions": [action_id]}}})

    first_final = lines[0]["finalSegment"]
    final_node = add_sound(3900001100, first_final["soundId"])
    add_action(3900003200, final_node, True)
    add_action(3900003210, final_node, False)
    add_event(f"Play_v{first_final['soundId']}", 3900003200)
    add_event(f"Stop_v{first_final['soundId']}", 3900003210)
    add_event(f"Play_v{first_final['stopAlias']}", 3900003210)

    for line in lines[1:]:
        index = line["index"]
        full_node = add_sound(3900001000 + index, line["soundId"])
        full_play = 3900003000 + index
        full_stop = 3900003100 + index
        add_action(full_play, full_node, True)
        add_action(full_stop, full_node, False)
        add_event(f"Play_v{line['soundId']}", full_play)
        add_event(f"Stop_v{line['soundId']}", full_stop)
        add_event(f"Play_v{line['stopAlias']}", full_stop)
        for cue_index, _ in enumerate(line["cues"]):
            carrier_id = line["carrierBase"] + cue_index
            cue_node = add_sound(3900002000 + index * 10 + cue_index, carrier_id)
            cue_play = 3900004000 + index * 10 + cue_index
            cue_stop = 3900005000 + index * 10 + cue_index
            add_action(cue_play, cue_node, True)
            add_action(cue_stop, cue_node, False)
            add_event(f"Play_v{carrier_id}", cue_play)
            add_event(f"Stop_v{carrier_id}", cue_stop)
    mixer["body"]["ActorMixer"]["children"]["items"] = [
        3900000001, *range(3900000010, 3900000015), *(item["id"]["Hash"] for item in new_sounds)]
    hirc["objects"] = [*original_sounds, *new_sounds, mixer, *original_actions, *new_actions,
                       *original_events, *new_events]
    hirc["object_count"] = len(hirc["objects"])
    graph_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = {"durations": durations, "cueSamples": cue_samples, "segmentHashes": segment_hashes,
               "segmentSamples": segment_samples, "mediaCount": len(media_waves),
               "objects": hirc["object_count"], "events": len(original_events) + len(new_events),
               "sourceHashes": source_hashes, "convertedHashes": converted_hashes,
               "convertedPeakDbfs": converted_peaks_dbfs,
               "wemHashes": {media_id: digest(BANK_DIR / f"{media_id}.wem") for media_id in media_waves}}
    (scratch / "prepared.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
