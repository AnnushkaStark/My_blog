from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Удалил лишнее
    path('', views.IndexPageView.as_view(), name='index'),
    path('reg/', views.RegisterView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('user/', views.LoginView.as_view(), name='user'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account_settings/', views.AccountSettingView.as_view(), name='settings'),
    path('change_mail/', views.ChangeEmail.as_view(), name='change_mail'),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
    path('add_bio/', views.AddBio.as_view(), name='add_bio')
]
