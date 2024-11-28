from django.urls import path
from . import views

urlpatterns = [
    path('' , views.PageQuestion.as_view()),
    path('<int:pk>/', views.UpdateQuestion.as_view()),
    path('easy/', views.Easy_Question.as_view()),
    path('normal/', views.Normal_Question.as_view()),
    path('hard/', views.Hard_Question.as_view()),
    path('new/', views.NewQuestions.as_view()),
    path('old/', views.OldQuestions.as_view()),
    path('answer/', views.AnswerQuestion.as_view()),

]
