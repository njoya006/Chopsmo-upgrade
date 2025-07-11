from rest_framework import serializers
from planner.models import NutritionInfo, DietaryRule, MealPlan, CustomUser  # Models in planner app
from recipes.models import Recipe, Ingredient  # Assuming Recipe and Ingredient are in recipes app

# Existing Serializers
class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']

class DietaryRuleSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = DietaryRule
        fields = ['id', 'name', 'description', 'include_ingredients', 'exclude_ingredients', 'min_ingredients']
        read_only_fields = ['id', 'user', 'created_at']

class NutritionInfoSerializer(serializers.ModelSerializer):
    recipe_id = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all(), source='recipe')

    class Meta:
        model = NutritionInfo
        fields = ['id', 'recipe', 'recipe_id', 'calories', 'protein', 'fat', 'carbs', 'fiber']
        read_only_fields = ['id', 'recipe', 'created_at']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'category', 'unit']

class MealPlanSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = MealPlan
        fields = ['id', 'user', 'recipe', 'date', 'meal_type', 'created_at']
        read_only_fields = ['id', 'created_at']

# New Serializer (added for grocery list feature)
class GroceryListItemSerializer(serializers.Serializer):
    name = serializers.CharField()
    category = serializers.CharField()
    quantity = serializers.FloatField()
    unit = serializers.CharField()