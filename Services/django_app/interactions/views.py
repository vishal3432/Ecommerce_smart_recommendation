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

        try:
            product = Product.objects.get(id=product_id)

            # ✅ Prevent anonymous crash
            if not user.is_authenticated:
                return Response({"error": "User not authenticated"}, status=401)

            # ✅ Avoid duplicate spam (update instead of create)
            Interaction.objects.update_or_create(
                user=user,
                product=product,
                defaults={"action": action}
            )

            return Response({"message": "Interaction saved"})

        except Product.DoesNotExist:
            return Response({"error": "Invalid product"}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


# ✅ KEEP (but improved slightly)
@csrf_exempt
def like_product(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        try:
            product = Product.objects.get(id=product_id)

            if not request.user.is_authenticated:
                return JsonResponse({"status": "unauthorized"}, status=401)

            Interaction.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={"action": "like"}
            )

            return JsonResponse({"status": "liked"})

        except Product.DoesNotExist:
            return JsonResponse({"status": "error"}, status=400)
