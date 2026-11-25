import json
import unittest

import baking


class TestBaking(unittest.TestCase):
    def test_cups_to_grams(self):
        self.assertAlmostEqual(baking.to_grams("all-purpose flour", 2, "cup"), 240)

    def test_tbsp_to_grams(self):
        self.assertAlmostEqual(baking.to_grams("water", 16, "tbsp"), 237)

    def test_unknown_ingredient(self):
        with self.assertRaises(KeyError):
            baking.to_grams("unobtainium", 1, "cup")

    def test_temperature(self):
        self.assertAlmostEqual(baking.f_to_c(350), 176.67, places=2)
        self.assertAlmostEqual(baking.c_to_f(180), 356)

    def test_scale(self):
        r = {"name": "x", "ingredients": {"flour": 100, "water": 60}}
        self.assertEqual(baking.scale_recipe(r, 2)["ingredients"], {"flour": 200, "water": 120})

    def test_bakers_percentages(self):
        with open("sourdough.json") as fh:
            recipe = json.load(fh)
        pct = baking.bakers_percentages(recipe)
        self.assertEqual(pct["bread flour"], 100.0)
        self.assertEqual(pct["water"], 70.0)
        self.assertEqual(pct["salt"], 2.0)

    def test_no_flour(self):
        with self.assertRaises(ValueError):
            baking.bakers_percentages({"name": "x", "ingredients": {"sugar": 10}})


if __name__ == "__main__":
    unittest.main()
