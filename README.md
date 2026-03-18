#  E-commerce Recommendation System

##  Problem statement

The task is to create an e-commerce web application using Django. This application will feature a product recommendation system powered by a machine learning model and  optimize certain calculations or model inference using Cython to improve performance.
---

## Architecture
SMART Recommendation System architecture (i.e, what is going in this project)
- Frontend (products.html) sends user interaction 
- Django handles API routing, user interaction storage, and acts as a bridge
- FastAPI handles ML recommendation logic asynchronously
- ML layer processes data using recommender system
- Database stores user interactions and product data
- Recommendations are sent back and UI refreshes dynamically

---

## Features

- Django → Handles UI, authentication, product management
- Product listing UI
- Like/Dislike interaction tracking
- FastAPI → ML recommendation updates
- REST API communication between services
- ML-based recommendation engine (TF-IDF + cosine similarity + spacy NER)

---

## Tech Stack

- Python
- Django (Used in business logic and Authentication via JWT)
- FastAPI (Sends User/Product data and request the recommendation)
- Scikit-learn
- SQLite
- HTML, CSS, JavaScript (Taken the help from  OpenAI to create an interactive Front-end )

---

## System Flow

1. User interacts with products (like/dislike)
2. Django sends interaction data to FastAPI
3. FastAPI processes data and generates recommendations
4. Django fetches and displays recommendations

---

## 🛠 Setup Instructions

## 1. For Django

cd Services/django_app

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python manage.py runserver


## 2. For FastAPI

cd Services/fastapi_service

pip install -r requirements.txt

uvicorn main:app --reload --port 8001


---


## Future Enhancement -
We can also integrate this project with AWS S3 which will serves the images and static files needed by the Project and can also be deployed using Docker on AWS EC2.
