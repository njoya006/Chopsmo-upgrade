# planner/models.py

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class MealPlan(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meal_plans')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='meal_plans')  # Updated to Recipe
    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        unique_together = ('user', 'date', 'meal_type')
        verbose_name = 'Meal Plan'
        verbose_name_plural = 'Meal Plans'

    def clean(self):
        # Prevent more than one meal of the same type per user per day
        if MealPlan.objects.exclude(pk=self.pk).filter(user=self.user, date=self.date, meal_type=self.meal_type).exists():
            raise ValidationError('You already have a meal plan for this meal type on this date.')

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title} ({self.meal_type}) on {self.date}"

# New Models
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True)  # e.g., Dairy, Produce
    unit = models.CharField(max_length=20, blank=True)  # e.g., grams, cups

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient.name} for {self.recipe.name}"

class GroceryList(models.Model):
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Grocery List for {self.meal_plan}"