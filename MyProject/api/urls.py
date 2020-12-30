from django.urls import path, include
from .views import article_list, article_detail, ArticleAPIView, ArticleDetailsView

urlpatterns = [
    # path('articles/', article_list, name="article-list"),
    path('articles/', ArticleAPIView.as_view(), name='article-list'),
    # path('detail/<int:pk>', article_detail, name="article-detail"),
    path('details/<int:id>/', ArticleDetailsView.as_view(), name="article-detail")
]