"""Fetch the Ventura urban tree dataset at its audited revision (shallow, single commit).

Git cannot fetch the abbreviated audited hash 78e81bd, so the full hash is pinned.
core.autocrlf is disabled so the original CSV bytes (CRLF) are preserved unchanged.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data" / "raw" / "ventura"
REPO = "https://github.com/jonathanventura/urban-tree-detection-data.git"
REVISION = "78e81bdbb484048472e77cbedd3afb49a6b621c6"  # audited as 78e81bd
EXPECTED_FILES = {"images": ("*.tif", 1651), "csv": ("*.csv", 1645), "json": ("*.json", 1645)}


def git(*args):
    result = subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=DEST, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed in {DEST}:\n{result.stderr.strip()}")
    return result.stdout.strip()


def fetch():
    DEST.mkdir(parents=True, exist_ok=True)
    git("init", "-q")
    git("config", "core.autocrlf", "false")
    git("remote", "add", "origin", REPO)
    git("fetch", "--depth", "1", "origin", REVISION)
    git("checkout", "-q", "--detach", REVISION)


def verify():
    head = git("rev-parse", "HEAD")
    if head != REVISION:
        raise SystemExit(f"{DEST} is at {head}, not the audited revision {REVISION}. It was not changed.")
    if git("status", "--porcelain"):
        raise SystemExit(f"{DEST} has local modifications; restore or delete it before preparing data.")
    for folder, (pattern, expected) in EXPECTED_FILES.items():
        found = len(list((DEST / folder).glob(pattern)))
        if found != expected:
            raise SystemExit(f"{DEST / folder}: found {found} {pattern} files, expected {expected}.")


def main():
    if (DEST / ".git").exists():
        print(f"Existing checkout found in {DEST}; verifying it without modification.")
    elif DEST.exists() and any(DEST.iterdir()):
        raise SystemExit(f"{DEST} exists but is not a Git checkout; refusing to overwrite it.")
    else:
        print(f"Fetching {REPO} at {REVISION} ...")
        fetch()
    verify()
    print(f"Ventura source verified at {REVISION}: " +
          ", ".join(f"{n} {folder}" for folder, (_, n) in EXPECTED_FILES.items()))


if __name__ == "__main__":
    main()
