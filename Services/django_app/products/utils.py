import requests

def get_recommendations():
    res = requests.get("http://127.0.0.1:8001/recommend")
    return res.json()