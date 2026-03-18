from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Interaction
from products.models import Product

class InteractionView(APIView):

    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        action = request.data.get("action")

        product = Product.objects.get(id=product_id)

        Interaction.objects.create(
            user=user,
            product=product,
            action=action
        )

        return Response({"message": "Interaction saved"})