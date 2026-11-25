"""Baking toolkit: unit conversion, recipe scaling, and baker's percentages.

Standard library only. Run `python baking.py --help` for the CLI.
"""

import argparse
import json
import sys

# Approximate grams per 1 US cup for common ingredients.
GRAMS_PER_CUP = {
    "all-purpose flour": 120,
    "bread flour": 127,
    "whole wheat flour": 113,
    "granulated sugar": 200,
    "brown sugar": 213,
    "powdered sugar": 120,
    "butter": 227,
    "water": 237,
    "milk": 244,
    "honey": 340,
    "cocoa powder": 85,
    "rolled oats": 90,
    "vegetable oil": 218,
}

# Volume units expressed in US cups.
VOLUME_IN_CUPS = {
    "cup": 1.0,
    "tbsp": 1 / 16,
    "tsp": 1 / 48,
}


def to_grams(ingredient: str, amount: float, unit: str) -> float:
    """Convert a volume amount of an ingredient to grams."""
    ingredient = ingredient.lower()
    unit = unit.lower()
    if ingredient not in GRAMS_PER_CUP:
        raise KeyError(f"Unknown ingredient: {ingredient!r}")
    if unit == "g":
        return amount
    if unit not in VOLUME_IN_CUPS:
        raise KeyError(f"Unknown unit: {unit!r}")
    return amount * VOLUME_IN_CUPS[unit] * GRAMS_PER_CUP[ingredient]


def f_to_c(f: float) -> float:
    return (f - 32) * 5 / 9


def c_to_f(c: float) -> float:
    return c * 9 / 5 + 32


def scale_recipe(recipe: dict, factor: float) -> dict:
    """Scale every ingredient amount in a recipe by `factor`."""
    return {
        "name": recipe["name"],
        "ingredients": {k: round(v * factor, 2) for k, v in recipe["ingredients"].items()},
    }


def bakers_percentages(recipe: dict, flour_keys=("flour",)) -> dict:
    """Return each ingredient as a percentage of total flour weight.

    Ingredients whose name contains any string in `flour_keys` count as flour.
    """
    ingredients = recipe["ingredients"]
    flour_total = sum(
        v for k, v in ingredients.items() if any(key in k.lower() for key in flour_keys)
    )
    if flour_total == 0:
        raise ValueError("No flour found in recipe")
    return {k: round(v / flour_total * 100, 1) for k, v in ingredients.items()}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Baking toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("grams", help="Convert a volume to grams")
    p.add_argument("ingredient")
    p.add_argument("amount", type=float)
    p.add_argument("unit", choices=["cup", "tbsp", "tsp"])

    p = sub.add_parser("temp", help="Convert oven temperature")
    p.add_argument("value", type=float)
    p.add_argument("to", choices=["c", "f"])

    p = sub.add_parser("scale", help="Scale a recipe JSON file")
    p.add_argument("file")
    p.add_argument("factor", type=float)

    p = sub.add_parser("percent", help="Baker's percentages for a recipe JSON file")
    p.add_argument("file")

    args = parser.parse_args(argv)

    if args.command == "grams":
        print(f"{to_grams(args.ingredient, args.amount, args.unit):.0f} g")
    elif args.command == "temp":
        out = f_to_c(args.value) if args.to == "c" else c_to_f(args.value)
        print(f"{out:.0f} °{args.to.upper()}")
    else:
        with open(args.file) as fh:
            recipe = json.load(fh)
        if args.command == "scale":
            result = scale_recipe(recipe, args.factor)
            print(json.dumps(result, indent=2))
        else:
            for name, pct in bakers_percentages(recipe).items():
                print(f"{name:<20}{pct:>6}%")


if __name__ == "__main__":
    sys.exit(main())
