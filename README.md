# E-commerce Smart Recommendation System

An AI-powered e-commerce web application that delivers **personalized product recommendations** based on real-time user interactions (like/dislike).

Built using a microservices architecture with **Django** for the main backend & UI, and **FastAPI** for high-performance ML recommendation logic.

---

## 🚀 Live Demo

**Website:** (https://ecommerce-smart-recommendation-crp8.onrender.com)

---

## Problem Statement

Create a full-stack e-commerce platform with an intelligent recommendation engine that learns from user behavior (likes/dislikes) to suggest relevant products. The system optimizes performance by separating concerns between Django and a dedicated FastAPI ML service.

---

## Architecture

The project follows a **microservices** approach:

- **Django App**: Handles frontend UI, user interactions, JWT authentication, product management, and acts as the API bridge.
- **FastAPI Service**: Dedicated high-performance service for ML-based recommendation logic (asynchronous processing).
- **Communication**: REST API between Django and FastAPI.
- **Database**: SQLite (easily scalable to PostgreSQL).

**System Flow:**
1. User browses products and interacts (like/dislike).
2. Django records the interaction and forwards data to FastAPI.
3. FastAPI processes the request using recommendation algorithms and returns personalized suggestions.
4. Django updates the UI dynamically.

---

## Features

- Modern and interactive product listing UI
- Real-time like/dislike tracking
- Personalized recommendations using **TF-IDF + Cosine Similarity + spaCy NER**
- RESTful API communication between services
- JWT-based authentication
- Responsive frontend with HTML, CSS & JavaScript
- Docker support for easy deployment

---

## Tech Stack

- **Backend**: Python, Django, FastAPI
- **Machine Learning**: scikit-learn (TF-IDF & Cosine Similarity), spaCy NER
- **Database**: SQLite #In future, can be upgraded to PostgreSQL for production
- **Frontend**: HTML, CSS, JavaScript #Used AI models to create this 
- **Deployment**: Docker, Render

---
## Challenges Faced

During the development of this project, several challenges were encountered, especially related to environment management and service integration.

### 1. Environment Management Issues
The biggest challenge was managing **two separate Python environments** for the microservices:

- Django App and FastAPI Service have **different dependencies**.
- Installing all packages in a single environment caused **version conflicts** (especially with `scikit-learn`, `spacy`, `django`, and `fastapi`).
- Running both services simultaneously often led to broken dependencies or import errors.

**Solution Implemented:**
- Created separate virtual environments and `requirements.txt` files for `django_app` and `fastapi_service`.
- Ran both services in parallel on different ports (Django on 8000, FastAPI on 8001).
- Used Docker with a `start.sh` script for unified deployment in production.

### 2. Common Errors Encountered

Here is a list of the major errors I faced and resolved during development:

- **ModuleNotFoundError**: `No module named 'django'` / `No module named 'fastapi'`  
  → Caused by running commands in the wrong virtual environment.

- **Port Already in Use** error (Port 8000 or 8001)  
  → When trying to run both services without proper port configuration.

- **Dependency Conflicts** (especially `numpy`, `scikit-learn`, and `spacy` versions)  
  → Occurred when trying to combine both services in one environment.

- **CORS Errors** when Django tried to call FastAPI endpoints  
  → Fixed by adding CORS middleware in FastAPI.

- **Connection Refused / Connection Timeout** to FastAPI from Django  
  → Happened when FastAPI was not running or running on the wrong port.

- **spaCy Model Not Found** (`en_core_web_sm` not downloaded)  
  → Fixed by running `python -m spacy download en_core_web_sm` in the FastAPI environment.

- **Static Files / Media Files not loading** in Django during deployment  
  → Resolved by proper `STATIC_ROOT` and `collectstatic` configuration.

- **Docker Build Failures** due to missing files or incorrect working directory in Dockerfile.

- **JWT Authentication token issues** during API calls between services.

---

## How These Challenges Were Overcome

- Strict separation of virtual environments for each service.
- Clear documentation of setup steps (running both services simultaneously).
- Added proper error handling and logging in both Django and FastAPI.
- Implemented Docker + `start.sh` script for consistent deployment.
- Used environment-specific `requirements.txt` files to avoid version conflicts.

----

## Future Enhancements

- Integrate AWS S3 for storing product images and static files
- Deploy using Docker on AWS EC2
- Add user registration and login page with improved UX
- Implement collaborative filtering along with content-based recommendations
- Migrate database to PostgreSQL for production use
