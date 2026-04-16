from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_recommendations(products, user_preferences=None, top_k=5):
    if not products:
        return []

    product_texts = [p.get("description", "") for p in products]

    # BUG FIX: fresh vectorizer per call — no shared global state / race conditions
    vectorizer = TfidfVectorizer()

    all_texts = product_texts + (user_preferences or [])

    # BUG FIX: guard against all-empty texts
    if not any(t.strip() for t in all_texts):
        return [p["id"] for p in products[:top_k]]

    matrix = vectorizer.fit_transform(all_texts)
    product_vectors = matrix[:len(products)]

    if user_preferences:
        user_vector = matrix[len(products):].mean(axis=0)
        similarity = cosine_similarity(user_vector, product_vectors)[0]
    else:
        # BUG FIX: use sum instead of mean for better differentiation in fallback
        sim_matrix = cosine_similarity(product_vectors, product_vectors)
        similarity = sim_matrix.sum(axis=0)

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

