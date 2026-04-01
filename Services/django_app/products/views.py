from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Product, Cart, CartItem, Order
from .recommendation_client import get_recommendations


# 👉 UI PAGE (UNCHANGED + SAFE)
def product_page(request):
    products = Product.objects.all()
    recommended_products = []

    query = request.GET.get("query", "")

    if query:
        data = get_recommendations(query, products)

        if "recommended_products" in data:
            recommended_products = Product.objects.filter(
                id__in=data["recommended_products"]
            )

    return render(request, "products.html", {
        "products": products,
        "recommended_products": recommended_products
    })


# 👉 API VIEW (UNCHANGED)
class RecommendationView(APIView):

    def get(self, request):
        query = request.GET.get("query", "")
        products = Product.objects.all()

        data = get_recommendations(query, products)

        return Response(data)


# =========================
# 🛒 CART FUNCTIONALITY
# =========================

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1

    item.save()

    return redirect("view_cart")


@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, "cart.html", {
        "items": items,
        "total": total
    })


# =========================
# 📦 CHECKOUT
# =========================

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    total = sum(item.product.price * item.quantity for item in items)

    # Create Order
    Order.objects.create(
        user=request.user,
        total_price=total
    )

    # Clear Cart
    items.delete()

    return render(request, "success.html", {
        "total": total
    })


# =========================
# 👍 👎 INTERACTION (HOOK)
# =========================

@login_required
def product_action(request, product_id, action):
    """
    This will later connect with interactions app
    Currently safe placeholder (no break)
    """
    return JsonResponse({
        "status": "success",
        "product_id": product_id,
        "action": action
    })
