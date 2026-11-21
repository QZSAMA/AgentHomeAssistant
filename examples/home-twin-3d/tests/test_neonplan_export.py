"""Interoperability regression checks for CAD -> official NeonPlan converter."""
import json
import math
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def fixture():
    return {
        "meta": {"units": "m", "wallHeight": 2.8},
        "footprint": [[0, 0], [7, 0], [7, 4], [0, 4]],
        "rooms": [
            {"id": "living", "name": "客厅", "polygon": [[0, 0], [4, 0], [4, 4], [0, 4]], "center": [2, 2]},
            {"id": "dining", "name": "餐厅", "polygon": [[4, 0], [7, 0], [7, 4], [4, 4]], "center": [5.5, 2]},
        ],
        # No physical wall on the semantic room boundary x=4.
        "walls": [{"id": "south", "a": [0, 4], "b": [7, 4], "thickness": .2, "height": 2.8}],
        "openings": [{"id": "window", "kind": "window", "a": [1, 0], "b": [3, 0], "height": 1.3, "sill": .9}],
        "furniture": [{"id": "table", "type": "table", "x": 5.5, "z": 2, "width": 1.6, "depth": .8, "height": .75, "rotation": math.pi / 2}],
    }


class NeonPlanExportTests(unittest.TestCase):
    def convert(self, house, devices=None, style=None):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        source = root / "house.json"
        source.write_text(json.dumps(house), encoding="utf-8")
        if devices is not None:
            (root / "devices.json").write_text(json.dumps({"devices": devices}), encoding="utf-8")
        if style is not None:
            (root / "design-style.json").write_text(json.dumps(style), encoding="utf-8")
        result = subprocess.run(
            ["python", str(ROOT / "scripts/export_neonplan.py"), "--source", str(source), "--out-dir", str(root)],
            capture_output=True, text=True, encoding="utf-8",
        )
        return root, result

    def test_official_roundtrip_preserves_rooms_scale_and_opening(self):
        root, result = self.convert(fixture())
        self.assertEqual(result.returncode, 0, result.stderr)
        simple = json.loads((root / "wuhan-neonplan-import.json").read_text(encoding="utf-8"))
        self.assertEqual(simple["units"], "m")
        self.assertEqual(simple["floors"][0]["rooms"][0]["points"][1], [4, 0])
        self.assertEqual(simple["floors"][0]["windows"][0]["width"], 2)
        backup = json.loads((root / "wuhan-neonplan-backup.json").read_text(encoding="utf-8"))
        self.assertEqual(backup["format"], "neonplan3d")
        floor = backup["building"]["floors"][0]
        self.assertEqual([r["name"] for r in floor["rooms"]], ["客厅", "餐厅"])
        self.assertEqual(len(floor["openings"]), 1)
        self.assertEqual(floor["openings"][0]["width"], 2)
        self.assertAlmostEqual(floor["furniture"][0]["w"], 1.6)
        self.assertAlmostEqual(floor["furniture"][0]["rotation"], 90)

    def test_open_plan_semantic_boundary_never_becomes_physical_wall(self):
        root, result = self.convert(fixture())
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((root / "neonplan-validation.json").read_text(encoding="utf-8"))
        self.assertEqual(report["generatedRoomBoundaryWalls"], 0)
        self.assertEqual(report["roomCount"], 2)
        self.assertTrue(report["officialParseExportPassed"])
        self.assertEqual(report["unhostedOpenings"], [])
        self.assertGreaterEqual(report["adjacentRoomPairs"], 1)

    def test_refuses_millimetres_instead_of_silently_scaling(self):
        house = fixture()
        house["meta"]["units"] = "mm"
        _, result = self.convert(house)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("metres", result.stderr)

    def test_real_backup_has_unbound_light_models_not_fabricated_entities(self):
        devices = [{"id": "living-main", "name": "测试主灯", "roomId": "living", "position": [2, 2.55, 2], "entityId": None}]
        root, result = self.convert(fixture(), devices)
        self.assertEqual(result.returncode, 0, result.stderr)
        backup = json.loads((root / "wuhan-neonplan-backup.json").read_text(encoding="utf-8"))
        lamps = [f for f in backup["building"]["floors"][0]["furniture"] if f["type"].startswith("lamp_")]
        self.assertEqual(len(lamps), 1)
        self.assertIsNone(lamps[0]["entity"])
        self.assertEqual(lamps[0]["id"], "lamp_living-main")

    def test_reference_style_preserves_layout_and_uses_effective_native_finishes(self):
        house = fixture()
        house["furniture"].append({"id": "living-sofa", "type": "sofa", "x": 2, "z": 2, "width": 2.1, "depth": .8, "height": .75, "rotation": .4})
        house["furniture"].append({"id": "bed", "type": "bed", "x": 1, "z": 1, "width": 1.5, "depth": 2, "height": .6, "rotation": 0})
        house["furniture"].append({"id": "kitchen", "type": "kitchen", "x": 6, "z": 1, "width": 1.5, "depth": .6, "height": .9, "rotation": 0})
        style = {
            "palette": {"wall": "#eee5d6", "white": "#ede9df"},
            "roomStyles": {"living": {"floor": "herringbone", "neonplanFloorMaterial": "oak", "wallColor": "#eee5d6"}},
            "furnitureStyles": {"living-sofa": {"finish": {"fabric": "#4d7e91", "wood": "#86603e"}}, "table": {"shape": "round-glass", "finish": {"wood": "#aeb6b2"}}},
            "wallStyles": {"south": {"kind": "wood-framed-glass", "baseHeight": .92, "glassTop": 2.35}},
            "decor": [{"id": "rug", "type": "rug", "x": 2, "z": 2, "width": 2, "depth": 1.5, "height": .025, "rotation": 0}]
        }
        style["furnitureStyles"]["bed"] = {"finish": {"fabric": "#bc8432", "wood": "#9b633a"}, "headboardFabric": "#b88630", "linenColor": "#b6c7c5"}
        style["furnitureStyles"]["kitchen"] = {"finish": {"wood": "#a97545"}, "counterColor": "#edece5", "upperCabinets": True}
        root, result = self.convert(house, style=style)
        self.assertEqual(result.returncode, 0, result.stderr)
        floor = json.loads((root / "wuhan-neonplan-backup.json").read_text(encoding="utf-8"))["building"]["floors"][0]
        self.assertEqual(floor["rooms"][0]["floor_material"], "oak")
        sofa = next(f for f in floor["furniture"] if f["id"] == "furn_living-sofa")
        self.assertEqual(sofa["finish"]["fabric"], "#4d7e91")
        self.assertAlmostEqual(sofa["rotation"], math.degrees(.4), places=3)
        self.assertEqual([sofa["x"], sofa["z"], sofa["w"], sofa["d"]], [2, 2, 2.1, .8])
        self.assertEqual(floor["walls"][0]["height"], 2.8)
        self.assertEqual(floor["walls"][0]["color"], "#eee5d6")
        self.assertEqual(len(floor["openings"]), 1)
        self.assertEqual(next(f for f in floor["furniture"] if f["id"] == "furn_table")["type"], "table_round")
        self.assertEqual(sum(f["id"] == "decor_rug" for f in floor["furniture"]), 1)
        self.assertEqual(next(f for f in floor["furniture"] if f["id"] == "furn_bed")["finish"]["fabric"], "#b6c7c5")
        self.assertEqual(next(f for f in floor["furniture"] if f["id"] == "furn_kitchen")["finish"]["wood"], "#edece5")
        # Exporting again consumes source data, not the previously decorated backup.
        rerun = subprocess.run(["python", str(ROOT / "scripts/export_neonplan.py"), "--source", str(root / "house.json"), "--out-dir", str(root)], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(rerun.returncode, 0, rerun.stderr)
        repeated = json.loads((root / "wuhan-neonplan-backup.json").read_text(encoding="utf-8"))["building"]["floors"][0]
        self.assertEqual(floor, repeated)
        report = json.loads((root / "neonplan-material-mapping.json").read_text(encoding="utf-8"))
        self.assertTrue(any("herringbone" in x for x in report["approximations"]))
        self.assertTrue(any("wood-framed-glass" in x for x in report["approximations"]))

    def test_wet_room_default_uses_recognized_tiles_enum(self):
        house = fixture()
        house["rooms"][0]["name"] = "卫生间"
        root, result = self.convert(house)
        self.assertEqual(result.returncode, 0, result.stderr)
        floor = json.loads((root / "wuhan-neonplan-backup.json").read_text(encoding="utf-8"))["building"]["floors"][0]
        self.assertEqual(floor["rooms"][0]["floor_material"], "tiles")


if __name__ == "__main__":
    unittest.main()
