from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexPageView.as_view()),
    path('home/', views.IndexPageView.as_view()),
    path('/', views.IndexPageView.as_view()),
    path('reg/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
]