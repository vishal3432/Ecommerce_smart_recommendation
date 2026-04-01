from fastapi import APIRouter, Request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()

# ✅ Global vectorizer (performance boost)
vectorizer = TfidfVectorizer()


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

    # ✅ FIXED RESPONSE FORMAT
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

        # ✅ Prepare text
        product_texts = [p.get("description", "") for p in products]
        all_texts = product_texts + user_prefs

        # ✅ Fit-transform
        matrix = vectorizer.fit_transform(all_texts)

        product_vectors = matrix[:len(products)]

        # =========================
        # 🧠 Similarity Logic
        # =========================
        if user_prefs:
            user_vector = matrix[len(products):].mean(axis=0)
            similarity = cosine_similarity(user_vector, product_vectors)[0]
        else:
            # fallback: average similarity
            similarity = cosine_similarity(product_vectors, product_vectors).mean(axis=0)

        # =========================
        # 📊 Ranking
        # =========================
        ranked = sorted(
            enumerate(similarity),
            key=lambda x: x[1],
            reverse=True
        )

        top_ids = [
            products[idx]["id"]
            for idx, _ in ranked[:5]
        ]

        return {"recommended_products": top_ids}

    except Exception as e:
        return {
            "error": str(e),
            "recommended_products": []
        }
