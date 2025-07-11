from collections import defaultdict
from .models import MealPlan, RecipeIngredient

def generate_grocery_list(meal_plan_id):
    try:
        meal_plan = MealPlan.objects.get(id=meal_plan_id)
        ingredient_map = defaultdict(lambda: {'quantity': 0, 'unit': '', 'category': ''})

        # Get the recipe from the meal plan and its ingredients
        recipe = meal_plan.recipe
        for recipe_ingredient in recipe.recipe_ingredients.all():
            ingredient = recipe_ingredient.ingredient
            key = f"{ingredient.name}_{recipe_ingredient.unit}"
            ingredient_map[key]['name'] = ingredient.name
            ingredient_map[key]['quantity'] += recipe_ingredient.quantity
            ingredient_map[key]['unit'] = recipe_ingredient.unit
            ingredient_map[key]['category'] = ingredient.category

        # Convert to list for API response
        return list(ingredient_map.values())
    except MealPlan.DoesNotExist:
        return [] 