from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Product, Cart, CartItem, Order
from .recommendation_client import get_recommendations


# 👉 UI PAGE
def product_page(request):
    products = Product.objects.all()
    recommended_products = []
    query = request.GET.get("query", "")

    if request.user.is_authenticated:
        # Always try to recommend based on likes
        data = get_recommendations(request.user, products)
        if "recommended_products" in data:
            recommended_products = Product.objects.filter(
                id__in=data["recommended_products"]
            )
    elif query:
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


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect("/admin/login/?next=/add-to-cart/" + str(product_id) + "/")
    
    # BUG FIX: use get_object_or_404 to avoid unhandled DoesNotExist 500 error
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect("view_cart")



def view_cart(request):
    # BUG FIX: view_cart had no auth check — crashed with AnonymousUser 500
    if not request.user.is_authenticated:
        return redirect("/admin/login/?next=/cart/")
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


def checkout(request):
    # BUG FIX: checkout had no auth check — crashed with AnonymousUser 500
    if not request.user.is_authenticated:
        return redirect("/admin/login/?next=/checkout/")

    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    # BUG FIX: compute total BEFORE deleting items (queryset is lazy)
    total = sum(item.product.price * item.quantity for item in items)

    # Create Order
    Order.objects.create(
        user=request.user,
        total_price=total
    )

    # Clear Cart — after total is computed
    cart.items.all().delete()

    return render(request, "success.html", {
        "total": total
    })


# =========================
# 👍 👎 INTERACTION (HOOK)
# =========================

@login_required
def product_action(request, product_id, action):
    # BUG FIX: validate action against allowed choices to prevent junk data
    VALID_ACTIONS = {"like", "dislike", "view"}
    if action not in VALID_ACTIONS:
        return JsonResponse({"status": "error", "detail": "Invalid action"}, status=400)

    try:
        from interactions.models import Interaction
        product = get_object_or_404(Product, id=product_id)
        Interaction.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={"action": action}
        )
        return JsonResponse({"status": "success", "action": action})
    except Exception as e:
        return JsonResponse({"status": "error", "detail": str(e)}, status=500)
