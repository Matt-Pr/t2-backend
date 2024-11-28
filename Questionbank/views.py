from django.shortcuts import render
from rest_framework import generics 
from .models import Question , User
from .serializers import QuestionSerializer , AnswerSerializer
from rest_framework.generics import ListCreateAPIView
# Create your views here.

class PageQuestion(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class UpdateQuestion(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'pk'

class AnswerQuestion(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AnswerSerializer

class Easy_Question(generics.ListAPIView):
    queryset = Question.objects.filter(choice='easy')
    serializer_class = QuestionSerializer

class Normal_Question(generics.ListAPIView):
    queryset = Question.objects.filter(choice='normal')
    serializer_class = QuestionSerializer

class Hard_Question(generics.ListAPIView):
    queryset = Question.objects.filter(choice='hard')
    serializer_class = QuestionSerializer

class NewQuestions(generics.ListAPIView):
    queryset = Question.objects.all().order_by('-date')[:10] 
    serializer_class = QuestionSerializer

class OldQuestions(generics.ListAPIView):
    queryset = Question.objects.all().order_by('date')[:10]
    serializer_class = QuestionSerializer
    