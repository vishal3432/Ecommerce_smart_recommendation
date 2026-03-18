from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_recommendations
from .models import Product
from .recommendation_client import get_recommendations

def product_page(request):
    products = Product.objects.all()

    recommended_products = []

    if request.user.is_authenticated:
        data = get_recommendations(request.user, products)

        if "recommended_products" in data:
            recommended_products = Product.objects.filter(
                id__in=data["recommended_products"]
            )

    return render(request, "products.html", {
        "products": products,
        "recommended_products": recommended_products
    })

class RecommendationView(APIView):

    def get(self, request):
        user = request.user
        products = Product.objects.all()
        data = get_recommendations(user, products)
        return Response(data)

