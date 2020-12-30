from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from rest_framework import generics
from rest_framework import mixins

from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from django.shortcuts import get_object_or_404

# Create your views here.


class ArticleViewSet(viewsets.ViewSet):
    
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True) # serializing all articles into objects
        return Response(serializer.data) # takes serialized data and sends response in JSON format

    def create(self, request):
        serializer = ArticleSerializer(data=request.data) # serializing in comming request data 

        if serializer.is_valid(): # checking validity
            serializer.save() # saving the serialized data into model instance
            return Response(serializer.data, status=status.HTTP_201_CREATED) # takes serialized data and sends response in JSON format
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # returning error 

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article) # serializing all articles into objects
        return Response(serializer.data) # takes serialized data and sends response in JSON format

    def update(self, request, pk=None):
        article = Article.objects.get(pk=pk)        
        serializer = ArticleSerializer(article, data=request.data) # serializing the article object with the parsed data 

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""""""""""""""""""""" Class Based Views """""""""""""""""""""


class GenericArticleView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    lookup_field = "id"

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)



class ArticleAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True) # serializing all articles into objects
        return Response(serializer.data) # takes serialized data and sends response in JSON format

    def post(self, request):
        serializer = ArticleSerializer(data=request.data) # serializing in comming request data 

        if serializer.is_valid(): # checking validity
            serializer.save() # saving the serialized data into model instance
            return Response(serializer.data, status=status.HTTP_201_CREATED) # takes serialized data and sends response in JSON format
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # returning error 


class ArticleDetailsView(APIView):

    def get_object(self, id):
        try:
            return Article.objects.get(id=id) # trying to find the article object matching the 'id' passed
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        """ GET Method to Get or Read the article from database """ 
        article = self.get_object(id)
        serializer = ArticleSerializer(article) # serializing the article object found 
        return Response(serializer.data) # returning serialized data into JSON format

    def put(self, request, id):
        """ PUT Method to Update the Article """
        article = self.get_object(id)        
        serializer = ArticleSerializer(article, data=request.data) # serializing the article object with the parsed data 

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)        
        article.delete() # deleting the article object found
        return Response(status=status.HTTP_204_NO_CONTENT)
        


""""""""""""""""""""" Function Based Views """""""""""""""""""""


# @csrf_exempt #allows post requests without csrf token
@api_view(['GET', 'POST']) # decorating views with django-rest-framework api views to add special functionalities
def article_list(request):

    if request.method == 'GET':
        """If method is GET"""
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True) # serializing all articles into objects
        return Response(serializer.data) # takes serialized data and sends response in JSON format

    elif request.method == "POST":
        """If method is POST"""
        # data = JSONParser().parse(request) # Parse JSON formatted data from in comming request object
        serializer = ArticleSerializer(data=request.data) # serializing in comming request data 

        if serializer.is_valid(): # checking validity
            serializer.save() # saving the serialized data into model instance
            return Response(serializer.data, status=status.HTTP_201_CREATED) # takes serialized data and sends response in JSON format
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # returning error 


# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE']) # decorating views with django-rest-framework api views to add special functionalities
def article_detail(request, pk):

    try:
        article = Article.objects.get(pk=pk) # trying to find the article object matching the 'pk' passed
    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = ArticleSerializer(article) # serializing the article object found 
        return Response(serializer.data) # returning serialized data into JSON format

    elif request.method == "PUT":
        # data = JSONParser().parse(request) # Parse JSON formatted data from in comming request object
        serializer = ArticleSerializer(article, data=request.data) # serializing the article object with the parsed data 

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        article.delete() # deleting the article object found
        return Response(status=status.HTTP_204_NO_CONTENT)
        

