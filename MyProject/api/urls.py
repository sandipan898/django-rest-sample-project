from django.urls import path, include
from .views import article_list, article_detail

urlpatterns = [
    path('articles/', article_list, name="article-list"),
    path('detail/<int:pk>', article_detail, name="article-detail"),
]