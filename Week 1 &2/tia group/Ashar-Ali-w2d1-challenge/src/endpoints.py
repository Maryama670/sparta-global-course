from src.recipe_data import recipe_list

REQUIRED_FIELDS = ("dish_name", "description", "ingredients_list", "rating")


def _find_recipe(dish_name):
    for recipe in recipe_list:
        if recipe["dish_name"] == dish_name:
            return recipe
    return None


def get_recipe(dish_name):
    recipe = _find_recipe(dish_name)
    if recipe is None:
        return {"message": f"{dish_name} not found"}
    return recipe


def post_new_recipe(recipe):
    missing_fields = [field for field in REQUIRED_FIELDS if not recipe.get(field)]
    if missing_fields:
        return {"message": f"failed: recipe missing required fields {missing_fields}"}

    recipe_list.append(
        {field: recipe[field] for field in REQUIRED_FIELDS}
    )
    return {"message": f"{recipe['dish_name']} added successfully"}


def get_all_recipes():
    return recipe_list


def change_recipe(dish_name, updates):
    recipe = _find_recipe(dish_name)
    if recipe is None:
        return {"message": f"failed: {dish_name} not found"}

    recipe.update(updates)
    return {"message": f"{dish_name} updated successfully"}


def remove_recipe(dish_name):
    recipe = _find_recipe(dish_name)
    if recipe is None:
        return {"message": f"{dish_name} not found"}

    recipe_list.remove(recipe)
    return {"dish_name": dish_name}
