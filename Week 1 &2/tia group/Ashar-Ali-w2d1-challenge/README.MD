# Recipe Box

Local, synthetic-data recipe API with 5 endpoints. See `SPEC.MD` for full requirements.

## Structure

- `src/recipe_data.py` - in-memory `recipe_list` with 5 synthetic recipes
- `src/endpoints.py` - the 5 endpoint functions
- `tests/test_endpoints.py` - acceptance tests

## Endpoints

| Function | Method | Description |
|---|---|---|
| `get_recipe(dish_name)` | GET | Return a recipe, or a not-found message |
| `post_new_recipe(recipe)` | POST | Add a recipe if it has all required fields |
| `get_all_recipes()` | GET | Return all recipes |
| `change_recipe(dish_name, updates)` | PUT | Update fields on an existing recipe |
| `remove_recipe(dish_name)` | DELETE | Remove a recipe, return its dish name |

A recipe has: `dish_name`, `description`, `ingredients_list`, `rating`.

# First CD into the folder Monday-API

# Install requirements.txt

pip install -r requirements.txt

# Run 9 tests or  Run Smoke test  in (on git bash )

```
python -m pytest tests/test_endpoints.py -q
```

```
bash smoke.sh 
```
