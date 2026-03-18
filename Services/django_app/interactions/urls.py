from django.urls import path
from .views import InteractionView

urlpatterns = [
    path("interact/", InteractionView.as_view()),
]