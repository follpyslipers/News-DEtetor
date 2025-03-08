from django.urls import path
from . import views
from .views import ClassifyNewsView


app_name ="detector"
urlpatterns = [
	path('', views.home, name='home'),
	path('detector/', views.predict_news, name='predict_news'),
    path("classify-news/", ClassifyNewsView.as_view(), name="classify-news"),
]