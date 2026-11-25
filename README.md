# Baking Toolkit

A small, dependency-free Python command-line tool for everyday baking math.

- Convert cups/tablespoons/teaspoons to grams for common ingredients
- Convert oven temperatures between °F and °C
- Scale a recipe up or down
- Calculate baker's percentages

## Requirements

Python 3.8+. No third-party packages.

## Usage

```bash
# Volume to grams
python baking.py grams "all-purpose flour" 2 cup      # 240 g

# Oven temperature
python baking.py temp 350 c                           # 177 °C

# Scale a recipe (JSON file) by 1.5x
python baking.py scale sourdough.json 1.5

# Baker's percentages
python baking.py percent sourdough.json
```

### Recipe format

```json
{
  "name": "Simple Sourdough Loaf",
  "ingredients": { "bread flour": 500, "water": 350, "salt": 10, "starter": 100 }
}
```

Amounts are in grams. Any ingredient with "flour" in its name counts toward the flour total for baker's percentages.

## Tests

```bash
python -m unittest
```

## Notes

Gram-per-cup values are approximations; weighing ingredients is always more accurate than measuring by volume.

## License

MIT
