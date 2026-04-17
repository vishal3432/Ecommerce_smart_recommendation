import os
import requests

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8001/recommend")


def get_recommendations(user_or_query, products):
    try:
        liked_descriptions = []

        # ✅ CASE 1: If user is logged in
        if hasattr(user_or_query, "is_authenticated") and user_or_query.is_authenticated:
            # BUG FIX: interaction_set is wrong — Interaction model uses default related_name
            # which is 'interaction_set', but we need to filter by action='like'
            from interactions.models import Interaction
            liked_interactions = Interaction.objects.filter(
                user=user_or_query, action='like'
            ).select_related('product')

            liked_descriptions = [
                interaction.product.description for interaction in liked_interactions
            ]

        # ✅ CASE 2: If query string (fallback)
        elif isinstance(user_or_query, str) and user_or_query:
            liked_descriptions = [user_or_query]

        # ✅ Prepare payload
        payload = {
            "products": [
                {"id": p.id, "description": p.description} for p in products
            ],
            "user_preferences": liked_descriptions
        }

        # ✅ Call FastAPI
        response = requests.post(FASTAPI_URL, json=payload, timeout=5)
        response.raise_for_status()

        return response.json()

     except Exception as e:
        # ✅ FALLBACK: FastAPI down → return first 5 products instead of empty
        return {
            "recommended_products": [p.id for p in list(products[:5])]
        }
