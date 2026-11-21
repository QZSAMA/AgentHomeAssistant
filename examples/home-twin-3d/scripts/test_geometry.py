"""Invariant tests for the CAD-derived house data; run after extraction."""
import json
import math
import unittest
from pathlib import Path

HOUSE = Path(__file__).resolve().parents[1] / "data" / "house.json"


class GeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.house = json.loads(HOUSE.read_text(encoding="utf-8")) if HOUSE.exists() else None

    def test_house_is_generated(self):
        self.assertIsNotNone(self.house, "CAD extraction must produce house.json")

    def test_units_and_real_outer_dimensions(self):
        if self.house is None:
            self.skipTest("Awaiting generated data")
        self.assertEqual(self.house["meta"]["units"], "m")
        xs, zs = zip(*self.house["footprint"])
        self.assertAlmostEqual(max(xs)-min(xs), 11.83, places=3)
        self.assertAlmostEqual(max(zs)-min(zs), 10.17, places=3)
        self.assertTrue(all(c["passed"] for c in self.house["meta"]["dimensionChecks"]))

    def test_entry_gap_is_not_filled_by_a_wall(self):
        if self.house is None:
            self.skipTest("Awaiting generated data")
        door = next(o for o in self.house["openings"] if o["id"] == "entry-door")
        self.assertAlmostEqual(math.dist(door["a"], door["b"]), 1.07, places=3)
        mx = (door["a"][0]+door["b"][0])/2
        mz = (door["a"][1]+door["b"][1])/2
        for wall in self.house["walls"]:
            a,b=wall["a"],wall["b"]
            if abs(a[1]-b[1])<0.001 and abs(a[1]-mz)<0.1:
                self.assertFalse(min(a[0],b[0]) < mx < max(a[0],b[0]), wall["id"])

    def test_core_rooms_are_defined_and_annotated(self):
        if self.house is None:
            self.skipTest("Awaiting generated data")
        rooms = {r["id"]:r for r in self.house["rooms"]}
        for room_id in ["living", "dining", "studio"]:
            self.assertTrue(rooms[room_id]["interactive"])
            self.assertGreaterEqual(len(rooms[room_id]["polygon"]), 3)
            self.assertTrue(rooms[room_id]["provenance"])
        self.assertGreater(len(self.house["cadLines"]), 500)

    def test_bedroom_bed_is_against_north_wall_and_east_window_side(self):
        if self.house is None:
            self.skipTest("Awaiting generated data")
        bed = next(f for f in self.house["furniture"] if f["id"] == "bedroom-bed")
        walls = {w["id"]:w for w in self.house["walls"]}
        north_inner = walls["outer-ne"]["a"][1] + walls["outer-ne"]["thickness"]/2
        east_inner = walls["outer-east-top"]["a"][0] - walls["outer-east-top"]["thickness"]/2
        self.assertEqual(bed["rotation"], 0, "Move the bed without rotating its headboard")
        self.assertAlmostEqual(bed["x"] + bed["width"]/2, east_inner, places=6)
        self.assertAlmostEqual(bed["z"] - bed["depth"]/2, north_inner, places=6)
        room = next(r for r in self.house["rooms"] if r["id"] == "bedroom")
        xs, zs = zip(*room["polygon"])
        self.assertGreaterEqual(bed["x"]-bed["width"]/2, min(xs))
        self.assertLessEqual(bed["x"]+bed["width"]/2, max(xs)+1e-6)
        self.assertGreaterEqual(bed["z"]-bed["depth"]/2, min(zs)-1e-6)
        self.assertLessEqual(bed["z"]+bed["depth"]/2, max(zs))

    def test_sofa_keeps_the_user_accepted_cad_pose(self):
        if self.house is None:
            self.skipTest("Awaiting generated data")
        sofa = next(f for f in self.house["furniture"] if f["id"] == "living-sofa")
        self.assertEqual(
            {k:sofa[k] for k in ("x","z","width","depth","height","rotation")},
            {"x":3.403896,"z":6.560656,"width":2.09,"depth":.7315,"height":.78,"rotation":0},
        )


if __name__ == "__main__":
    unittest.main()
