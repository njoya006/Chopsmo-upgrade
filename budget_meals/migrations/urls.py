from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_meal_home, name='budget_meals_home'),
    path('api/suggest/', views.suggest_meals, name='suggest_meals'),
]