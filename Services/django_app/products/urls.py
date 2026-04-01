from django.urls import path
from .views import (
    product_page,
    RecommendationView,
    add_to_cart,
    view_cart,
    checkout,
    product_action
)

urlpatterns = [
    # ✅ Existing routes (UNCHANGED)
    path("", product_page, name="product_page"),
    path("recommend/", RecommendationView.as_view(), name="recommend_api"),

    # 🛒 Cart routes
    path("cart/", view_cart, name="view_cart"),
    path("add-to-cart/<int:product_id>/", add_to_cart, name="add_to_cart"),

    # 📦 Checkout
    path("checkout/", checkout, name="checkout"),

    # 👍 👎 Interaction (future-ready)
    path("action/<int:product_id>/<str:action>/", product_action, name="product_action"),
]
