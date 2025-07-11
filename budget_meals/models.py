from django.db import models
from django.core.validators import MinValueValidator

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('ml', 'Milliliter'),
        ('pc', 'Piece'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    
    def __str__(self):
        return f"{self.name} ({self.price_per_unit} XAF per {self.unit})"

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    serving_size = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    
    class Meta:
        unique_together = ('recipe', 'ingredient')
    
    def __str__(self):
        return f"{self.quantity}{self.ingredient.unit} {self.ingredient.name} in {self.recipe.name}"