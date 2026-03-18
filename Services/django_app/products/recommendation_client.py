import requests

FASTAPI_URL = "http://127.0.0.1:8001/recommend"

def get_recommendations(user, products):

    liked_products = user.interaction_set.filter(action='like')

    liked_descriptions = [
        interaction.product.description
        for interaction in liked_products
    ]

    payload = {
        "products": [
            {"description": p.description}
            for p in products
        ],
        "user_preferences": liked_descriptions
    }

    response = requests.post(FASTAPI_URL, json=payload)

    return response.json()