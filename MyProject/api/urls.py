from django.urls import path, include
from .views import article_list
urlpatterns = [
    path('articles/', article_list, name="article-list"),
]