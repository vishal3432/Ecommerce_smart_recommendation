import os
import requests

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8001/recommend")


def get_recommendations(user, products):
    try:
        # Get liked products
        liked_products = user.interaction_set.filter(action='like')

        liked_descriptions = [
            interaction.product.description for interaction in liked_products
        ]

        # Prepare payload
        payload = {
            "products": [
                {"id": p.id, "description": p.description} for p in products
            ],
            "user_preferences": liked_descriptions
        }

        # Call FastAPI
        response = requests.post(FASTAPI_URL, json=payload, timeout=5)

        response.raise_for_status()

        return response.json()

    except Exception as e:
        return {"error": str(e), "recommended_products": []}json()
