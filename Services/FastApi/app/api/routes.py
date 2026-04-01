from fastapi import APIRouter, Request
from ml.recommender import compute_recommendations

router = APIRouter()


# =========================
# 🔹 GET (Fallback)
# =========================
@router.get("/recommend")
def recommend_get(query: str):
    query = query.lower()

    if "phone" in query:
        ids = [1, 2]
    elif "laptop" in query:
        ids = [4]
    elif "shoes" in query:
        ids = [8]
    else:
        ids = [1, 3, 5]

    return {"recommended_products": ids}


# =========================
# 🔹 POST (ML Logic)
# =========================
@router.post("/recommend")
async def recommend_post(request: Request):
    try:
        data = await request.json()

        products = data.get("products", [])
        user_prefs = data.get("user_preferences", [])

        if not products:
            return {"recommended_products": []}

        # ✅ Use ML module (clean architecture)
        top_ids = compute_recommendations(products, user_prefs)

        return {"recommended_products": top_ids}

    except Exception as e:
        return {
            "error": str(e),
            "recommended_products": []
        }
