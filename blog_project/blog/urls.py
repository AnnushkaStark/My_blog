from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexPageView.as_view()),
    path('home/', views.IndexPageView.as_view()),
    path('/', views.IndexPageView.as_view()),
    path('reg/', views.RegisterView.as_view()) ,
    path('login/', views.LoginView.as_view()),
    path('user/', views.LoginView.as_view(),name='user' ),
    path('logout/', views.LogoutView.as_view() ,name='logout'),
    path('account_settings/', views.AccountSettingView.as_view(), name='settings'),
    path('change_mail/', views.ChangeEamail.as_view(), name='change_mail')
]