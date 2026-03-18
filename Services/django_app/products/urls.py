from django.urls import path
from .views import product_page
from .views import RecommendationView

urlpatterns = [
    path("recommend/", RecommendationView.as_view()),
    path("", product_page),
]