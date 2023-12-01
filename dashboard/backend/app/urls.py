from django.urls import path, re_path
from app import views

urlpatterns = [
    path('index/', views.index),
]