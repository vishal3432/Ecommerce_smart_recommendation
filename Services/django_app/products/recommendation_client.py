import os
import requests

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8001/recommend")


def get_recommendations(user_or_query, products):
    try:
        liked_descriptions = []

        # ✅ CASE 1: If user is logged in
        if hasattr(user_or_query, "is_authenticated") and user_or_query.is_authenticated:
            liked_products = user_or_query.interaction_set.filter(action='like')

            liked_descriptions = [
                interaction.product.description for interaction in liked_products
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
        return {
            "error": str(e),
            "recommended_products": []
        }
