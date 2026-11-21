"""Download the pinned NEON Tree Evaluation archives and verify their Zenodo MD5 checksums.

Source: Zenodo record 5914554 (NeonTreeEvaluation v0.2.2, DOI 10.5281/zenodo.5914554).
The separate training.zip archive is deliberately not downloaded.
"""
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "neon"
RECORD_API = "https://zenodo.org/api/records/5914554"
VERSION = "0.2.2"
# Pinned from Zenodo metadata (checked 2026-11-21); re-checked against live metadata on every run.
FILES = {
    "annotations.zip": (560_984, "f577f0948a259d474ee0199fb8d76524"),
    "evaluation.zip": (3_853_532_101, "f0c444fc59cf0115ce8c981a576fab77"),
}
CHUNK = 1 << 20


def md5sum(path):
    digest = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def download_urls():
    """Confirm the live Zenodo record still matches the pinned release; return file URLs."""
    with urllib.request.urlopen(RECORD_API, timeout=60) as response:
        record = json.load(response)
    if record["metadata"].get("version") != VERSION:
        raise SystemExit(f"Zenodo record version is {record['metadata'].get('version')!r}, expected {VERSION}.")
    live = {f["key"]: f for f in record["files"]}
    for name, (size, md5) in FILES.items():
        entry = live.get(name)
        if entry is None or entry["size"] != size or entry["checksum"] != f"md5:{md5}":
            raise SystemExit(f"Live Zenodo metadata for {name} does not match the pinned size/MD5: {entry}")
    return {name: live[name]["links"]["self"] for name in FILES}


def fetch_file(name, url):
    size, md5 = FILES[name]
    dest, part = OUT / name, OUT / f"{name}.part"
    if dest.exists():
        if dest.stat().st_size == size and md5sum(dest) == md5:
            return "already present, MD5 verified"
        raise SystemExit(f"{dest} exists but does not match the pinned size/MD5. It was not overwritten; inspect or delete it.")
    done = part.stat().st_size if part.exists() else 0
    if done > size:
        raise SystemExit(f"{part} is larger than the expected {size} bytes; delete it and rerun.")
    if done < size:
        headers = {"Range": f"bytes={done}-"} if done else {}
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120) as response:
            if done and response.status != 206:
                raise SystemExit(f"Server did not resume {name}; delete {part} and rerun.")
            with open(part, "ab") as f:
                for block in iter(lambda: response.read(CHUNK), b""):
                    f.write(block)
    if part.stat().st_size != size or md5sum(part) != md5:
        raise SystemExit(f"{part} failed size/MD5 verification. Delete it and rerun.")
    part.rename(dest)  # only a verified, complete file ever receives the final name
    return "downloaded, MD5 verified"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    urls = download_urls()
    for name in FILES:
        print(f"{name}: {fetch_file(name, urls[name])}")
    print(f"NEON Tree Evaluation v{VERSION} archives ready in {OUT}")


if __name__ == "__main__":
    main()
