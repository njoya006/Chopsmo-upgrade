from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('name', 'estimated_cost', 'difficulty', 'preparation_time')
    search_fields = ('name', 'description')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_unit', 'unit')
    search_fields = ('name',)
    list_filter = ('unit',)

admin.site.register(RecipeIngredient)