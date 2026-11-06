"""MEDIQ Dataset Loader — quick helper to load the dataset into pandas."""

import glob
import hashlib
import json
import os
import re
import pandas as pd

SAFE_SHARD_RE = re.compile(r"^mediq_part\d{3,}\.json$")
SAFE_CSV_RE = re.compile(r"^mediq_csv_part\d{3,}\.csv$")


def _sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def load_mediq(path=None, format="csv"):
    """Load MEDIQ dataset as a pandas DataFrame.

    Args:
        path: Path to the MEDIQ repo root. Defaults to parent of scripts/.
        format: 'csv' or 'json'. Default 'csv'.

    Returns:
        pandas.DataFrame with columns:
            id, question, answer, timestamp, consent,
            consentTimestamp, language_detected, ...
    """
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..")

    data_dir = os.path.join(path, "data")

    if format == "csv":
        csv_full_path = os.path.join(data_dir, "mediq_full.csv")
        if os.path.exists(csv_full_path):
            return pd.read_csv(csv_full_path, parse_dates=["timestamp", "consentTimestamp"])

        # Check for sharded CSVs
        shard_files = sorted([
            os.path.join(data_dir, f) for f in os.listdir(data_dir)
            if SAFE_CSV_RE.match(f)
        ])
        if shard_files:
            dfs = [pd.read_csv(sf, parse_dates=["timestamp", "consentTimestamp"]) for sf in shard_files]
            return pd.concat(dfs, ignore_index=True)

        raise FileNotFoundError(
            f"No CSV data found in {data_dir} (neither mediq_full.csv nor mediq_csv_part*.csv exist)"
        )

    # format == 'json'
    manifest_path = os.path.join(data_dir, "mediq_manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as mf:
            manifest = json.load(mf)

        if manifest.get("schemaVersion") != 1:
            raise ValueError(f"Unsupported manifest schemaVersion: {manifest.get('schemaVersion')}")

        shards = manifest.get("shards", [])
        if not shards:
            raise ValueError("Manifest has no shards listed")

        rows = []
        for s in shards:
            fname = s.get("filename", "")
            if not SAFE_SHARD_RE.match(fname):
                raise ValueError(f"Unsafe shard filename in manifest: {fname}")

            shard_path = os.path.join(data_dir, fname)
            if not os.path.exists(shard_path):
                raise FileNotFoundError(f"Missing shard file: {shard_path}")

            actual_size = os.path.getsize(shard_path)
            if actual_size != s.get("bytes"):
                raise ValueError(
                    f"Shard size mismatch for {fname}: expected {s.get('bytes')}, got {actual_size}"
                )

            expected_sha = s.get("sha256")
            if expected_sha and _sha256(shard_path) != expected_sha:
                raise ValueError(f"SHA-256 hash mismatch for shard {fname}")

            with open(shard_path, "r", encoding="utf-8") as sf:
                shard_data = json.load(sf)

            for date_str, entries in shard_data.get("data", {}).items():
                for entry in entries:
                    entry_copy = dict(entry)
                    entry_copy["date"] = date_str
                    rows.append(entry_copy)

        df = pd.DataFrame(rows)
        if not df.empty:
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601")
            if "consentTimestamp" in df.columns:
                df["consentTimestamp"] = pd.to_datetime(df["consentTimestamp"], format="ISO8601")
        return df

    # Fallback to legacy mediq_full.json
    legacy_json_path = os.path.join(data_dir, "mediq_full.json")
    if os.path.exists(legacy_json_path):
        with open(legacy_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        rows = []
        for date_str, entries in data.get("data", {}).items():
            for entry in entries:
                entry_copy = dict(entry)
                entry_copy["date"] = date_str
                rows.append(entry_copy)

        df = pd.DataFrame(rows)
        if not df.empty:
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601")
            if "consentTimestamp" in df.columns:
                df["consentTimestamp"] = pd.to_datetime(df["consentTimestamp"], format="ISO8601")
        return df

    raise FileNotFoundError(
        f"No JSON data found in {data_dir} (neither mediq_manifest.json nor mediq_full.json exist)"
    )


if __name__ == "__main__":
    df = load_mediq()
    print(f"Loaded {len(df)} entries")
    if "language_detected" in df.columns:
        print(f"\nHeuristic language distribution:")
        print(df["language_detected"].value_counts())
    if "ai_language" in df.columns:
        print(f"\nAI language distribution (corrected):")
        print(df["ai_language"].value_counts())
        print(f"\nAI intent distribution:")
        print(df["ai_intent"].value_counts())
        print(f"\nMedical relevance:")
        print(df["ai_medical_relevance"].value_counts())
        print(f"\nUser types:")
        print(df["ai_user_type_guess"].value_counts())
    if "timestamp" in df.columns and not df.empty:
        print(f"\nDate range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    if not df.empty:
        print(f"\nSample entry:")
        print(df.iloc[0].to_dict())
