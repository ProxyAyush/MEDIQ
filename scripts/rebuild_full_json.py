#!/usr/bin/env python3
"""Reconstruct the legacy full JSON dataset from MEDIQ shards.

Usage:
    python scripts/rebuild_full_json.py [--input-dir data/] [--output /tmp/mediq_full.json]
"""

import argparse
import hashlib
import json
import os
import re
import sys

SAFE_SHARD_RE = re.compile(r"^mediq_part\d{3,}\.json$")


def _sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def rebuild_full_json(data_dir, output_file=None):
    manifest_path = os.path.join(data_dir, "mediq_manifest.json")
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_path, "r", encoding="utf-8") as mf:
        manifest = json.load(mf)

    if manifest.get("schemaVersion") != 1:
        raise ValueError(f"Unsupported schemaVersion: {manifest.get('schemaVersion')}")

    shards = manifest.get("shards", [])
    if not shards:
        raise ValueError("Manifest has no shards listed")

    all_data = {}
    total_entries_count = 0

    for s in shards:
        fname = s.get("filename", "")
        if not SAFE_SHARD_RE.match(fname):
            raise ValueError(f"Unsafe shard filename: {fname}")

        shard_path = os.path.join(data_dir, fname)
        if not os.path.exists(shard_path):
            raise FileNotFoundError(f"Missing shard file: {shard_path}")

        actual_size = os.path.getsize(shard_path)
        if actual_size != s.get("bytes"):
            raise ValueError(f"Size mismatch for {fname}: expected {s.get('bytes')}, got {actual_size}")

        expected_sha = s.get("sha256")
        if expected_sha and _sha256(shard_path) != expected_sha:
            raise ValueError(f"SHA-256 hash mismatch for {fname}")

        with open(shard_path, "r", encoding="utf-8") as sf:
            shard_data = json.load(sf)

        for date_str, entries in shard_data.get("data", {}).items():
            if date_str not in all_data:
                all_data[date_str] = []
            all_data[date_str].extend(entries)
            total_entries_count += len(entries)

    if total_entries_count != manifest.get("totalEntries"):
        raise ValueError(
            f"Entry count mismatch: expected {manifest.get('totalEntries')}, assembled {total_entries_count}"
        )

    full_dataset = {
        "lastUpdated": manifest.get("lastUpdated"),
        "totalEntries": total_entries_count,
        "totalDates": len(all_data),
        "data": all_data,
    }

    if output_file:
        # Check safety: do not overwrite tracked source tree unintentionally
        out_abs = os.path.abspath(output_file)
        if os.path.abspath(data_dir) == os.path.dirname(out_abs) and os.path.basename(out_abs) == "mediq_full.json":
            print(
                "WARNING: Writing to data/mediq_full.json in repository. "
                "Ensure this is not committed back to git.",
                file=sys.stderr
            )

        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(full_dataset, out, indent=2, ensure_ascii=False)
            out.write("\n")
        print(f"Successfully reconstructed legacy JSON to {output_file} ({total_entries_count} records, {len(all_data)} dates)")

    return full_dataset


def main():
    parser = argparse.ArgumentParser(description="Reconstruct legacy full MEDIQ JSON from shards.")
    parser.add_argument(
        "--input-dir",
        default=os.path.join(os.path.dirname(__file__), "..", "data"),
        help="Path to data directory containing mediq_manifest.json and shards"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to output reconstructed JSON file"
    )
    args = parser.parse_args()

    try:
        rebuild_full_json(args.input_dir, args.output)
    except Exception as e:
        print(f"Error rebuilding dataset: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
