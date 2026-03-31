from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .recommendation_client import get_recommendations


# 👉 UI PAGE
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


# 👉 API VIEW
class RecommendationView(APIView):

    def get(self, request):
        query = request.GET.get("query", "")
        products = Product.objects.all()

        data = get_recommendations(query, products)

        return Response(data)
