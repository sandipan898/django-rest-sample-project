from django import urls
from django.urls import path, include
from .views import article_list, article_detail, ArticleAPIView, ArticleDetailsView, GenericArticleView, ArticleViewSet, ArticleGenericViewSet, ArticleModelViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register('articles', ArticleViewSet, basename='articles')
# router.register('articles', ArticleGenericViewSet, basename='articles')
router.register('articles', ArticleModelViewSet, basename='articles')


urlpatterns = [
    path('viewset/', include(router.urls)), # this will available at 'viewset/articles'
    path('viewset/<int:pk>/', include(router.urls)), # this will available at 'viewset/articles/:pk'
    # path('articles/', article_list, name="article-list"),
    path('articles/', ArticleAPIView.as_view(), name='article-list'),
    path('generic/articles/', GenericArticleView.as_view(), name='article-list'),
    path('generic/articles/<int:id>/', GenericArticleView.as_view(), name='article-list'),
    
    # path('detail/<int:pk>', article_detail, name="article-detail"),
    path('details/<int:id>/', ArticleDetailsView.as_view(), name="article-detail")
]