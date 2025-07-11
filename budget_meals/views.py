from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Recipe
from django.db.models import F, Sum

def budget_meal_home(request):
    return render(request, 'budget_meals/home.html')

@api_view(['GET'])
def suggest_meals(request):
    try:
        budget = float(request.GET.get('budget', 0))
        if budget <= 0:
            return Response({"error": "Budget must be positive"}, status=400)
            
        # Annotate recipes with their calculated cost
        recipes = Recipe.objects.annotate(
            calculated_cost=Sum(F('recipeingredient__quantity') * F('recipeingredient__ingredient__price_per_unit'))
        ).filter(calculated_cost__lte=budget).order_by('-calculated_cost')
        
        results = []
        for recipe in recipes:
            results.append({
                'id': recipe.id,
                'name': recipe.name,
                'cost': float(recipe.calculated_cost),
                'serving_size': recipe.serving_size,
                'cost_per_serving': float(recipe.calculated_cost / recipe.serving_size),
                'preparation_time': recipe.preparation_time,
                'difficulty': recipe.get_difficulty_display(),
            })
            
        return Response({'meals': results})
        
    except ValueError:
        return Response({"error": "Invalid budget value"}, status=400)