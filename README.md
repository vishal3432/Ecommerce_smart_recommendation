#  E-commerce Recommendation System

##  Problem statement
You are tasked with creating an e-commerce web application using Django. This application will feature a product recommendation system powered by a machine learning model. You will optimize certain calculations or model inference using Cython to improve performance.
---

## 🏗 Architecture

- Django → Handles UI, authentication, product management
- FastAPI → ML recommendation 
- REST API communication between services

---

## ⚙️ Features

- User authentication (Django)
- Product listing UI
- Like/Dislike interaction tracking
- Real-time recommendation updates
- ML-based recommendation engine (TF-IDF / similarity)

---

## 🧠 Tech Stack

- Python
- Django
- FastAPI
- Scikit-learn
- SQLite
- HTML, CSS, JavaScript (Taken the help from )

---

## 🔄 System Flow

1. User interacts with products (like/dislike)
2. Django sends interaction data to FastAPI
3. FastAPI processes data and generates recommendations
4. Django fetches and displays recommendations

---

## 🛠 Setup Instructions

### 1. Clone repo

```bash
git clone https://github.com/yourusername/AI-Ecommerce-Recommendation-System.git
cd AI-Ecommerce-Recommendation-System
