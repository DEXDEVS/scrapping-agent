from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scraper_app.urls')),  # Includes all URLs from scraper_app
]

