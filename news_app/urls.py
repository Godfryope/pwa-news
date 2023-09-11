from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),
    path('subscribe/', subscribe, name='subscribe'),
]