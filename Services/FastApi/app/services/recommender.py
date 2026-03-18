from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(products):
    texts = [p["description"] for p in products]

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(matrix)

    return similarity.tolist()