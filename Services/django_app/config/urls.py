from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🛍 Frontend (UI)
    path("", include("products.urls")),

    # 🔗 API routes (clean separation)
    path("api/products/", include("products.urls")),

    # 👍 👎 Interactions
    path("interactions/", include("interactions.urls")),
]
