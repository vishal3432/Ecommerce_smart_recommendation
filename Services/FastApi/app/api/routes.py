from fastapi import APIRouter
from app.services.recommender import compute_similarity

router = APIRouter()
@router.post("/recommend")
def recommend(data: dict):

    products = data["products"]
    user_prefs = data["user_preferences"]

    all_texts = [p["description"] for p in products] + user_prefs

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(all_texts)

    product_vectors = matrix[:len(products)]
    user_vector = matrix[len(products):].mean(axis=0)

    similarity = cosine_similarity(user_vector, product_vectors)

    ranked = sorted(
        list(enumerate(similarity[0])),
        key=lambda x: x[1],
        reverse=True
    )

    top_products = [idx for idx, _ in ranked[:5]]

    return {"recommended_products": top_products}