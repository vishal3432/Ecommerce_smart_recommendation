from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Interaction
from products.models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def like_product(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        try:
            product = Product.objects.get(id=product_id)

            Interaction.objects.create(
                user=request.user,
                product=product,
                action="like"
            )

            return JsonResponse({"status": "liked"})
        except:
            return JsonResponse({"status": "error"}, status=400)
