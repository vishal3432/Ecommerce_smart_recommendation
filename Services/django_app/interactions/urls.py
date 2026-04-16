from django.urls import path
from .views import InteractionView
from .views import like_product

urlpatterns = [
    path("interact/", InteractionView.as_view()),
    path("like/", like_product),
]
