from fastapi import APIRouter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()

@router.post("/recommend")
def recommend(data: dict):
    products = data.get("products", [])
    user_prefs = data.get("user_preferences", [])

    if not products:
        return {"recommended_products": []}

    all_texts = [p["description"] for p in products] + user_prefs
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(all_texts)
    product_vectors = matrix[:len(products)]

    if user_prefs:
        user_vector = matrix[len(products):].mean(axis=0)
        similarity = cosine_similarity(user_vector, product_vectors)[0]
    else:
        similarity = cosine_similarity(product_vectors, product_vectors).mean(axis=0)

    ranked = sorted(enumerate(similarity), key=lambda x: x[1], reverse=True)
    top_ids = [products[idx]["id"] for idx, _ in ranked[:5]]
    return {"recommended_products": top_ids}
