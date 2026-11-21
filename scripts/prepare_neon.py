"""Build the 193-image NEON evaluation subset from the pinned v0.2.2 archives.

Eligible images are those with both annotations/<id>.xml (image-annotated crowns) and
evaluation/RGB/<id>.tif. This excludes the training-tile XMLs and the field-crown/stem
imagery, which have no image-annotated XML.
"""
import csv
import io
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "neon"
OUT = ROOT / "data" / "prepared" / "neon"
SOURCE_VERSION = "NeonTreeEvaluation v0.2.2 (Zenodo 10.5281/zenodo.5914554)"
GSD_M = 0.1
EXPECTED = {"xml": 226, "rgb": 2289, "matched": 194, "final": 193}
EXCLUDED = {"SJER_016_2018": "inside hand-annotated 1 km training tile 2018_SJER_3_258000_4106000_image"}
NOTES = {
    "2018_SJER_3_252000_4113000_image_323": "UNRESOLVED: shares 1 km AOP tile 252000_4113000 with training "
    "crop 2018_SJER_3_252000_4113000_image_310; spatial overlap not verified",
}
FIELDS = ["image_id", "dataset", "source_id", "location_id", "site", "year", "image_path", "reference_path",
          "reference_type", "reference_count", "gsd_m", "width", "height", "source_version",
          "annotation_origin", "notes"]
PLOT = re.compile(r"([A-Z]{4})_(\d{3})_(\d{4})")
TILE_CROP = re.compile(r"(\d{4})_([A-Z]{4})_\d+_\d+_\d+_image_\d+")


def members(archive, folder, suffix):
    """Map identifier -> member path for files directly inside folder (macOS '._' artefacts ignored)."""
    found = {}
    for name in archive.namelist():
        match = re.fullmatch(rf"{folder}/([^/]+){re.escape(suffix)}", name)
        if match and not match[1].startswith("._"):
            found[match[1]] = name
    return found


def site_year(image_id):
    if match := PLOT.fullmatch(image_id):
        return match[1], match[3], f"{match[1]}_{match[2]}"
    if match := TILE_CROP.fullmatch(image_id):
        return match[2], match[1], image_id
    raise SystemExit(f"Unrecognised NEON image identifier: {image_id}")


def count_boxes(xml_bytes, width, height, image_id):
    count = 0
    for obj in ET.fromstring(xml_bytes).iter("object"):
        box = obj.find("bndbox")
        x0, y0, x1, y1 = (float(box.find(k).text) for k in ("xmin", "ymin", "xmax", "ymax"))
        if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
            raise SystemExit(f"{image_id}: box {(x0, y0, x1, y1)} is invalid for a {width}x{height} image.")
        count += 1
    return count


def main():
    if OUT.exists() and any(OUT.iterdir()):
        raise SystemExit(f"{OUT} already contains prepared data; delete it deliberately to rebuild.")
    with zipfile.ZipFile(RAW / "annotations.zip") as ann, zipfile.ZipFile(RAW / "evaluation.zip") as ev:
        xmls, rgbs = members(ann, "annotations", ".xml"), members(ev, "evaluation/RGB", ".tif")
        matched = sorted(set(xmls) & set(rgbs))
        found = {"xml": len(xmls), "rgb": len(rgbs), "matched": len(matched)}
        if found != {k: EXPECTED[k] for k in found} or not set(EXCLUDED) <= set(matched):
            raise SystemExit(f"Unexpected NEON source inventory {found}; expected {EXPECTED}.")
        selected = [i for i in matched if i not in EXCLUDED]
        if len(selected) != EXPECTED["final"]:
            raise SystemExit(f"Expected {EXPECTED['final']} images after exclusion, found {len(selected)}.")
        (OUT / "images").mkdir(parents=True, exist_ok=True)
        (OUT / "annotations").mkdir(exist_ok=True)
        rows = []
        for image_id in selected:
            png, xml = OUT / "images" / f"{image_id}.png", OUT / "annotations" / f"{image_id}.xml"
            with Image.open(io.BytesIO(ev.read(rgbs[image_id]))) as im:
                if im.mode != "RGB":
                    raise SystemExit(f"{image_id}: expected an 8-bit RGB TIFF, got mode {im.mode}.")
                width, height = im.size
                im.save(png, format="PNG")  # lossless, original pixel dimensions
            xml_bytes = ann.read(xmls[image_id])
            count = count_boxes(xml_bytes, width, height, image_id)
            xml.write_bytes(xml_bytes)  # original annotation, byte for byte
            site, year, location = site_year(image_id)
            rows.append({"image_id": image_id, "dataset": "neon", "source_id": image_id, "location_id": location,
                         "site": site, "year": year, "image_path": png.relative_to(ROOT).as_posix(),
                         "reference_path": xml.relative_to(ROOT).as_posix(), "reference_type": "box",
                         "reference_count": count, "gsd_m": GSD_M, "width": width, "height": height,
                         "source_version": SOURCE_VERSION, "annotation_origin": "copied",
                         "notes": NOTES.get(image_id, "")})
    with open(OUT / "manifest.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Prepared {len(rows)} NEON images ({sum(r['reference_count'] for r in rows)} reference crowns, "
          f"{len({r['site'] for r in rows})} sites); excluded {sorted(EXCLUDED)}.")


if __name__ == "__main__":
    main()
