from django.shortcuts import render , redirect
from . import models
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import News, User 
from .serializers import NewsSerializer , UserSerializer
# Create your views here.

class Page(ListCreateAPIView):
    queryset = News.objects.order_by("date").all()
    serializer_class = NewsSerializer

class UpdateNews(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'pk'

class NewsList(generics.ListCreateAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        news_id = self.kwargs.get('news_id')
        if news_id:
            return News.objects.filter(pk__gt=news_id)

class New_News(generics.ListAPIView):
    queryset = News.objects.all().order_by('-date')[:10] 
    serializer_class = NewsSerializer

class Old_News(generics.ListAPIView):
    queryset = News.objects.all().order_by('date')[:10]
    serializer_class = NewsSerializer
    