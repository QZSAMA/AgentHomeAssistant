"""Convert the measured house into NeonPlan using its pinned, unmodified importer.

The house's room polygons are semantic floor zones, not physical wall centrelines.
The native backup therefore disables their generated walls and uses surveyed walls.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=ROOT / "data/house.json")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "exports")
    args = parser.parse_args()
    house = json.loads(args.source.read_text(encoding="utf-8-sig"))
    if house.get("meta", {}).get("units") != "m":
        raise ValueError("Source coordinates must explicitly be in metres (meta.units='m').")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    aliases = {"dining_table": "table", "diningTable": "table", "cabinet": "sideboard", "bar": "island", "toilet": "wc", "vanity": "washbasin", "refrigerator": "fridge"}
    floor = {
        "name": "武汉印 · 住宅层", "elevation": 0,
        "height": max((w.get("height", 2.8) for w in house["walls"]), default=2.8),
        "rooms": [{"name": r["name"], "points": r["polygon"]} for r in house["rooms"]],
        "walls": [{"from": w["a"], "to": w["b"], "thickness": w.get("thickness", .2), "height": w.get("height", 2.8)} for w in house["walls"]],
        "doors": [], "windows": [], "furniture": [],
    }
    for opening in house.get("openings", []):
        if opening["kind"] not in ("door", "window"):
            continue
        a, b = opening["a"], opening["b"]
        item = {"at": [(a[0]+b[0])/2, (a[1]+b[1])/2], "width": round(math.dist(a, b), 6), "height": opening.get("height", 2.1)}
        if opening["kind"] == "window":
            item["sill"] = opening.get("sill", .9)
        floor["windows" if opening["kind"] == "window" else "doors"].append(item)
    for item in house.get("furniture", []):
        floor["furniture"].append({"name": item.get("name", item["type"]), "type": aliases.get(item["type"], item["type"]), "at": [item["x"], item["z"]], "width": item["width"], "depth": item["depth"], "height": item["height"], "rotation": round(math.degrees(item.get("rotation", 0)), 6)})
    simple = {"format": "neonplan-import", "units": "m", "rooms_at": "centre", "floors": [floor]}
    simple_path = args.out_dir / "wuhan-neonplan-import.json"
    simple_path.write_text(json.dumps(simple, ensure_ascii=False, indent=2), encoding="utf-8")
    subprocess.run(["node", str(ROOT / "scripts/run_neonplan_import.mjs"), str(simple_path), str(args.source.resolve()), str(args.out_dir.resolve())], check=True)

    # Same validation schema as the v4.0.0 Home Assistant backend, without HA.
    sys.path.insert(0, str(ROOT / "vendor/python-deps"))
    spec = importlib.util.spec_from_file_location("neonplan_schema", ROOT / "vendor/neonplan/custom_components/neonplan3d/schema.py")
    schema = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(schema)
    backup = json.loads((args.out_dir / "wuhan-neonplan-backup.json").read_text(encoding="utf-8"))
    schema.BUILDING_SCHEMA(backup["building"])
    report_path = args.out_dir / "neonplan-validation.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["officialBackendSchemaPassed"] = True
    report["backendSchema"] = "NeonPlan v4.0.0 schema.py BUILDING_SCHEMA; voluptuous 0.15.2"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Verified NeonPlan backup: {args.out_dir / 'wuhan-neonplan-backup.json'}")


if __name__ == "__main__":
    main()
