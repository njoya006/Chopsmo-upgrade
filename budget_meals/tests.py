from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Ingredient, Recipe
from .views import suggest_meals

class BudgetMealTests(TestCase):
    def setUp(self):
        self.rice = Ingredient.objects.create(
            name="Rice", 
            price_per_unit=500, 
            unit="kg"
        )
        self.chicken = Ingredient.objects.create(
            name="Chicken", 
            price_per_unit=2000, 
            unit="kg"
        )
        self.recipe = Recipe.objects.create(
            name="Rice and Chicken",
            preparation_time=30,
            difficulty="easy",
            serving_size=4
        )
        self.recipe.ingredients.add(self.rice, through_defaults={'quantity': 0.5})
        self.recipe.ingredients.add(self.chicken, through_defaults={'quantity': 0.25})

    def test_recipe_cost_calculation(self):
        # Recipe should cost (0.5*500) + (0.25*2000) = 250 + 500 = 750 XAF
        self.assertEqual(self.recipe.recipeingredient_set.count(), 2)
        calculated_cost = sum(
            ri.quantity * ri.ingredient.price_per_unit 
            for ri in self.recipe.recipeingredient_set.all()
        )
        self.assertEqual(calculated_cost, 750)

    def test_api_endpoint(self):
        url = reverse('suggest_meals') + "?budget=1000"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data['meals']) > 0)
        self.assertEqual(response.data['meals'][0]['name'], "Rice and Chicken")

    def test_invalid_budget(self):
        url = reverse('suggest_meals') + "?budget=abc"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)from django.test import TestCase

