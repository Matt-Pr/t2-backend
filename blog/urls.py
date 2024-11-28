from django.urls import path
from . import views


urlpatterns = [
    path('',views.Page.as_view()),
    path('<int:pk>/',views.UpdateNews.as_view()),
    path('<int:news_id>/', views.NewsList.as_view()),
    path('new/', views.New_News.as_view()),
    path('old/', views.Old_News.as_view()),
]