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

# Create your views here.

# @csrf_exempt #allows post requests without csrf token
@api_view(['GET', 'POST'])
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
@api_view(['GET', 'PUT', 'DELETE'])
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
        