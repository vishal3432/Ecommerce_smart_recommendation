from fastapi import APIRouter, Request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()

# ✅ GET version (for Django query-based call)
@router.get("/recommend")
def recommend_get(query: str):
    # Dummy fallback logic (since no products passed)
    if "phone" in query.lower():
        return {"ids": [1, 2]}
    elif "laptop" in query.lower():
        return {"ids": [4]}
    elif "shoes" in query.lower():
        return {"ids": [8]}
    else:
        return {"ids": [1, 3, 5]}


# ✅ POST version (your original ML logic)
@router.post("/recommend")
async def recommend_post(request: Request):
    data = await request.json()

    products = data.get("products", [])
    user_prefs = data.get("user_preferences", [])

    if not products:
        return {"recommended_products": []}

    # Prepare text data
    all_texts = [p["description"] for p in products] + user_prefs

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(all_texts)

    product_vectors = matrix[:len(products)]

    # Compute similarity
    if user_prefs:
        user_vector = matrix[len(products):].mean(axis=0)
        similarity = cosine_similarity(user_vector, product_vectors)[0]
    else:
        similarity = cosine_similarity(product_vectors, product_vectors).mean(axis=0)

    # Rank products
    ranked = sorted(enumerate(similarity), key=lambda x: x[1], reverse=True)
    top_ids = [products[idx]["id"] for idx, _ in ranked[:5]]

    return {"recommended_products": top_ids}
