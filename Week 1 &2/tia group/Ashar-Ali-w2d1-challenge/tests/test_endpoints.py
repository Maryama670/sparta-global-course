import copy

import pytest

from src import recipe_data
from src.endpoints import (
    change_recipe,
    get_all_recipes,
    get_recipe,
    post_new_recipe,
    remove_recipe,
)


@pytest.fixture(autouse=True)
def reset_recipe_list():
    original = copy.deepcopy(recipe_data.recipe_list)
    yield
    recipe_data.recipe_list[:] = original


# get_recipe (GET)

def test_get_recipe_returns_recipe_when_dish_found():
    result = get_recipe("Chocolate Cake")
    assert result["dish_name"] == "Chocolate Cake"
    assert result["description"]
    assert result["ingredients_list"]
    assert result["rating"]


def test_get_recipe_returns_not_found_message_when_dish_missing():
    result = get_recipe("Nonexistent Dish")
    assert "message" in result
    assert "not found" in result["message"].lower()


# post_new_recipe (POST)

def test_post_new_recipe_adds_recipe_with_all_required_fields():
    new_recipe = {
        "dish_name": "Veggie Stir Fry",
        "description": "Mixed vegetables stir fried in soy sauce",
        "ingredients_list": "Broccoli, carrot, pepper, soy sauce, garlic",
        "rating": "4 out of 5",
    }
    post_new_recipe(new_recipe)
    all_recipes = get_all_recipes()
    assert any(r["dish_name"] == "Veggie Stir Fry" for r in all_recipes)


def test_post_new_recipe_rejects_recipe_missing_required_fields():
    incomplete_recipe = {
        "dish_name": "Mystery Dish",
        "description": "Missing ingredients and rating",
    }
    result = post_new_recipe(incomplete_recipe)
    assert "message" in result
    assert "success" not in result["message"].lower() or "fail" in result["message"].lower()
    all_recipes = get_all_recipes()
    assert not any(r["dish_name"] == "Mystery Dish" for r in all_recipes)


# get_all_recipes (GET)

def test_get_all_recipes_returns_all_recipes_in_list():
    all_recipes = get_all_recipes()
    assert len(all_recipes) == len(recipe_data.recipe_list)
    dish_names = {r["dish_name"] for r in all_recipes}
    assert "Chocolate Cake" in dish_names
    assert "Margherita Pizza" in dish_names


# change_recipe (PUT)

def test_change_recipe_updates_existing_recipe_fields():
    result = change_recipe("Chocolate Cake", {"ingredients_list": "Egg, flour, sugar, cocoa"})
    assert "message" in result
    assert "success" in result["message"].lower()

    updated = get_recipe("Chocolate Cake")
    assert updated["ingredients_list"] == "Egg, flour, sugar, cocoa"


def test_change_recipe_returns_failed_message_when_dish_missing():
    result = change_recipe("Nonexistent Dish", {"rating": "1 out of 5"})
    assert "message" in result
    assert "fail" in result["message"].lower()


# remove_recipe (DELETE)

def test_remove_recipe_removes_dish_and_returns_dish_name():
    result = remove_recipe("Beef Tacos")
    assert result["dish_name"] == "Beef Tacos"
    all_recipes = get_all_recipes()
    assert not any(r["dish_name"] == "Beef Tacos" for r in all_recipes)


def test_remove_recipe_returns_not_found_message_when_dish_missing():
    result = remove_recipe("Nonexistent Dish")
    assert "message" in result
    assert "not found" in result["message"].lower()
