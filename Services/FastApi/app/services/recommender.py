from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Global vectorizer (reuse for performance)
vectorizer = TfidfVectorizer()


def compute_recommendations(products, user_preferences=None, top_k=5):
    if not products:
        return []

    #  Extract product descriptions safely
    product_texts = [p.get("description", "") for p in products]

    # Combine texts
    all_texts = product_texts + (user_preferences or [])

    # Vectorize
    matrix = vectorizer.fit_transform(all_texts)

    product_vectors = matrix[:len(products)]

    # =========================
    # 🧠 Similarity Logic
    # =========================
    if user_preferences:
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
        for idx, _ in ranked[:top_k]
    ]

    return top_ids
