"""Assemble the frozen 500-image benchmark_v1 from the two prepared datasets (offline only).

Images are copied as source-prefixed PNGs; NEON XML boxes and Ventura CSV points are copied
unchanged in their original formats. The build is written to a staging directory and renamed
only after all checks pass, and an existing benchmark_v1 is never overwritten.
"""
import csv
import hashlib
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PREPARED = ROOT / "data" / "prepared"
OUT = ROOT / "data" / "benchmark_v1"
STAGING = ROOT / "data" / "benchmark_v1.partial"
SELECTION = ROOT / "docs" / "benchmark_v1_selection.csv"  # version-controlled list of expected source IDs
EXPECTED = {"neon": (193, "box", ".xml"), "ventura": (307, "point", ".csv")}
FIELDS = ["image_id", "dataset", "source_id", "location_id", "site", "year", "image_path", "reference_path",
          "reference_type", "reference_count", "gsd_m", "width", "height", "source_version",
          "annotation_origin", "notes", "image_sha256", "reference_sha256"]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(dataset):
    count, ref_type, suffix = EXPECTED[dataset]
    with open(PREPARED / dataset / "manifest.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != count:
        raise SystemExit(f"{dataset}: manifest has {len(rows)} rows, expected {count}.")
    for row in rows:
        image, ref = ROOT / row["image_path"], ROOT / row["reference_path"]
        if row["dataset"] != dataset or row["reference_type"] != ref_type or ref.suffix != suffix:
            raise SystemExit(f"{dataset}/{row['source_id']}: unexpected dataset, reference type or file format.")
        if not image.is_file() or not ref.is_file():
            raise SystemExit(f"{dataset}/{row['source_id']}: missing image or annotation file.")
        with Image.open(image) as im:
            if im.format != "PNG" or im.mode != "RGB" or im.size != (int(row["width"]), int(row["height"])):
                raise SystemExit(f"{image}: expected an RGB PNG of {row['width']}x{row['height']}.")
    return rows


def main():
    if OUT.exists():
        raise SystemExit(f"{OUT} already exists and is frozen; it was not modified. Build a new version instead.")
    if STAGING.exists():
        raise SystemExit(f"{STAGING} exists from an interrupted build; inspect and delete it, then rerun.")
    rows = load("neon") + load("ventura")
    ids = [f"{r['dataset']}__{r['source_id']}" for r in rows]
    if len(set(ids)) != 500:
        raise SystemExit(f"Expected 500 unique image identifiers, found {len(set(ids))}.")
    with open(SELECTION, newline="", encoding="utf-8") as f:
        expected = {(r["dataset"], r["source_id"], r["source_version"]) for r in csv.DictReader(f)}
    actual = {(r["dataset"], r["source_id"], r["source_version"]) for r in rows}
    if actual != expected:
        raise SystemExit(f"Prepared images differ from {SELECTION.name}: {len(actual - expected)} unexpected, "
                         f"{len(expected - actual)} missing.")
    (STAGING / "images").mkdir(parents=True)
    (STAGING / "annotations").mkdir()
    final = []
    for image_id, row in zip(ids, rows):
        ref_suffix = Path(row["reference_path"]).suffix
        image_dst = STAGING / "images" / f"{image_id}.png"
        ref_dst = STAGING / "annotations" / f"{image_id}{ref_suffix}"
        shutil.copyfile(ROOT / row["image_path"], image_dst)
        shutil.copyfile(ROOT / row["reference_path"], ref_dst)
        final.append({**row, "image_id": image_id,
                      "image_path": (OUT / "images" / image_dst.name).relative_to(ROOT).as_posix(),
                      "reference_path": (OUT / "annotations" / ref_dst.name).relative_to(ROOT).as_posix(),
                      "image_sha256": sha256(image_dst), "reference_sha256": sha256(ref_dst)})
    totals = {d: sum(r["dataset"] == d for r in final) for d in EXPECTED}
    if totals != {d: n for d, (n, _, _) in EXPECTED.items()} or len(list((STAGING / "images").iterdir())) != 500:
        raise SystemExit(f"Final totals check failed: {totals}")
    with open(STAGING / "manifest.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(final)
    STAGING.rename(OUT)
    print(f"benchmark_v1 frozen at {OUT}: {totals['neon']} NEON + {totals['ventura']} Ventura = 500 images.")


if __name__ == "__main__":
    main()
