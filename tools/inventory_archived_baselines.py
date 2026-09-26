"""Inventory catalogued runtime paths in the two archived game-file folders."""

import argparse
import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CATALOG = REPO / "asset-catalog.json"
OUTPUT = REPO / "docs" / "baselines" / "archived-game-files.json"
ARCHIVE_ROOT = Path("Z:/Backup/Elden Ring/ER Base Files")
LABELS = ("1.16", "1.17")


def fingerprint(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return {"status": "present", "sizeBytes": path.stat().st_size,
            "sha256": digest.hexdigest()}


def inventory():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    files = []
    for group in catalog["groups"]:
        for relative in group["files"]:
            item = {"package": group["package"], "group": group["id"],
                    "path": relative, "archives": {}}
            for label in LABELS:
                candidate = ARCHIVE_ROOT / label / relative
                item["archives"][label] = (
                    fingerprint(candidate) if candidate.is_file()
                    else {"status": "missing"}
                )
            files.append(item)
    return {
        "schemaVersion": 1,
        "catalog": "asset-catalog.json",
        "catalogSha256": hashlib.sha256(CATALOG.read_bytes()).hexdigest(),
        "archiveRoot": str(ARCHIVE_ROOT).replace("\\", "/"),
        "archiveLabels": list(LABELS),
        "method": "For each catalog group file, test exact relative path beneath each archive label; hash present regular files with SHA-256 and record byte size.",
        "provenance": "Folder labels only; game build and clean vanilla state independently unverified.",
        "files": files,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare fresh inventory with the saved JSON")
    args = parser.parse_args()
    result = inventory()
    rendered = json.dumps(result, indent=2, ensure_ascii=True) + "\n"
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != rendered:
            parser.exit(1, "Archived baseline inventory differs from saved JSON.\n")
        print("Archived baseline inventory matches saved JSON.")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(rendered, encoding="utf-8")
        counts = {label: sum(item["archives"][label]["status"] == "present"
                             for item in result["files"]) for label in LABELS}
        print(f"Saved {len(result['files'])} catalog paths; present by archive: {counts}")


if __name__ == "__main__":
    main()
