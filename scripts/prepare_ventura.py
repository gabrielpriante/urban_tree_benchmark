"""Select and prepare 307 Ventura 2020 images, one per geographic location.

Sampling: all Bishop (10) and Eureka (21) locations, plus 46 per remaining city drawn with
random.Random(20261121) from index-sorted candidates, cities processed in alphabetical order.
Point annotations are copied unchanged. The source README states that a missing CSV means
the image has no trees; such images receive a header-only CSV marked 'absent_in_source'.
"""
import csv
import json
import random
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image
from rasterio.enums import ColorInterp

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "ventura"
OUT = ROOT / "data" / "prepared" / "ventura"
REVISION = "78e81bdbb484048472e77cbedd3afb49a6b621c6"
SEED, YEAR, PER_CITY, TAKE_ALL = 20261121, "2020", 46, {"bishop", "eureka"}
EXPECTED_2020 = {"bishop": 10, "chico": 99, "claremont": 92, "eureka": 21, "long_beach": 100,
                 "palm_springs": 100, "riverside": 90, "santa_monica": 92}
GSD_M, TOTAL = 0.6, 307
NAME = re.compile(r"([a-z_]+)_(\d{4})_(\d+)")
FIELDS = ["image_id", "dataset", "source_id", "location_id", "site", "year", "image_path", "reference_path",
          "reference_type", "reference_count", "gsd_m", "width", "height", "source_version",
          "annotation_origin", "notes"]


def candidates_2020():
    if not (RAW / ".git").exists():
        raise SystemExit(f"{RAW} is not a Ventura checkout; run scripts/fetch_ventura.py first.")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=RAW, capture_output=True, text=True).stdout.strip()
    if head != REVISION:
        raise SystemExit(f"{RAW} is at {head or 'no revision'}, expected {REVISION}; run fetch_ventura.py.")
    by_city = {}
    for tif in (RAW / "images").glob("*.tif"):
        match = NAME.fullmatch(tif.stem)
        if not match:
            raise SystemExit(f"Unexpected Ventura image name: {tif.name}")
        if match[2] == YEAR:
            by_city.setdefault(match[1], []).append(int(match[3]))
    if {city: len(v) for city, v in by_city.items()} != EXPECTED_2020:
        raise SystemExit(f"Unexpected 2020 inventory: { {c: len(v) for c, v in by_city.items()} }")
    return {city: sorted(v) for city, v in sorted(by_city.items())}  # 604 locations, one image each


def select(by_city):
    rng = random.Random(SEED)
    chosen = [(c, i) for c, idx in by_city.items() for i in (idx if c in TAKE_ALL else sorted(rng.sample(idx, PER_CITY)))]
    if len(chosen) != TOTAL or len(set(chosen)) != TOTAL:
        raise SystemExit(f"Selection produced {len(chosen)} images ({len(set(chosen))} unique locations).")
    return chosen


def to_png(tif, png):
    with rasterio.open(tif) as src:
        if src.count != 4 or set(src.dtypes) != {"uint8"}:
            raise SystemExit(f"{tif.name}: expected 4 uint8 bands, found {src.count} {src.dtypes}.")
        if tuple(src.colorinterp[:3]) != (ColorInterp.red, ColorInterp.green, ColorInterp.blue):
            raise SystemExit(f"{tif.name}: bands 1-3 are {src.colorinterp[:3]}, not red/green/blue.")
        rgb = np.ascontiguousarray(src.read([1, 2, 3]).transpose(1, 2, 0))  # band 4 (NIR) dropped
    image = Image.fromarray(rgb)
    if image.mode != "RGB":
        raise SystemExit(f"{tif.name}: conversion produced mode {image.mode}.")
    image.save(png, format="PNG")
    return image.size


def copy_points(source_id, width, height, dest):
    src_csv, src_json = RAW / "csv" / f"{source_id}.csv", RAW / "json" / f"{source_id}.json"
    if not src_csv.exists():
        if src_json.exists():
            raise SystemExit(f"{source_id}: JSON exists without CSV; source inventory is inconsistent.")
        dest.write_bytes(b"x,y\r\n")  # documented empty image; no points invented
        return 0, "absent_in_source"
    with open(src_csv, newline="") as f:
        rows = list(csv.reader(f))
    if not rows or rows[0] != ["x", "y"]:
        raise SystemExit(f"{src_csv.name}: missing 'x,y' header.")
    for row in rows[1:]:
        if len(row) != 2 or not all(v.isdigit() for v in row) or not (int(row[0]) < width and int(row[1]) < height):
            raise SystemExit(f"{src_csv.name}: invalid point {row} for a {width}x{height} image.")
    with open(src_json, encoding="utf-8") as f:
        if len(json.load(f)["features"]) != len(rows) - 1:
            raise SystemExit(f"{source_id}: CSV and GeoJSON point counts differ.")
    shutil.copyfile(src_csv, dest)
    return len(rows) - 1, "copied"


def main():
    if OUT.exists() and any(OUT.iterdir()):
        raise SystemExit(f"{OUT} already contains prepared data; delete it deliberately to rebuild.")
    (OUT / "images").mkdir(parents=True, exist_ok=True)
    (OUT / "annotations").mkdir(exist_ok=True)
    rows = []
    for city, index in select(candidates_2020()):
        source_id = f"{city}_{YEAR}_{index}"
        png, ref = OUT / "images" / f"{source_id}.png", OUT / "annotations" / f"{source_id}.csv"
        width, height = to_png(RAW / "images" / f"{source_id}.tif", png)
        count, origin = copy_points(source_id, width, height, ref)
        rows.append({"image_id": source_id, "dataset": "ventura", "source_id": source_id,
                     "location_id": f"{city}_{index}", "site": city, "year": YEAR,
                     "image_path": png.relative_to(ROOT).as_posix(), "reference_path": ref.relative_to(ROOT).as_posix(),
                     "reference_type": "point", "reference_count": count, "gsd_m": GSD_M, "width": width,
                     "height": height, "source_version": f"urban-tree-detection-data@{REVISION}",
                     "annotation_origin": origin, "notes": ""})
    with open(OUT / "manifest.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    empty = [r["source_id"] for r in rows if r["annotation_origin"] == "absent_in_source"]
    print(f"Prepared {len(rows)} Ventura images ({sum(r['reference_count'] for r in rows)} reference points; "
          f"source images without trees: {empty or 'none'}).")


if __name__ == "__main__":
    main()
