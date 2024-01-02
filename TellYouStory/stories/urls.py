from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("", views.IndexPageView.as_view(), name="index"),
    path("register/", views.RegisterPageView.as_view(), name="register"),
    path("form_register/", views.UserRegistrationViwe.as_view(), name="register_form"),
    path("login/", views.UserLoginView.as_view(), name="login_page"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("login_form/", views.UserLoginFormView.as_view(), name="login_form"),
    path("user/", views.UserPageView.as_view(), name="user_page"),
]
