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
    path("account_settings/", views.SettingsPage.as_view(), name="settings_page"),
    path(
        "private_settings/",
        views.PrivateSettingsPage.as_view(),
        name="private_settings_page",
    ),
    path("deactivate/", views.DeactivatePage.as_view(), name="deactivate_page"),
    path("change_mail/", views.ChangeMailFormView.as_view(), name="change_mail"),
    path(
        "change_password/",
        views.ChangePasswordFormView.as_view(),
        name="change_password",
    ),
    path(
        "deactivate_form/", views.DeactivateFormView.as_view(), name="deactivate_form"
    ),
    path("change_name/", views.NameChangeFormView.as_view(), name="change_name"),
    path("change_town/", views.TownChangeFormView.as_view(), name="change_town"),
    path(
        "change_birth_date/",
        views.ChangeBirthDateFormView.as_view(),
        name="change_birth_date",
    ),
    path("link_change/", views.ChangeLinkFormView.as_view(), name="link_change"),
    path("avatar_change/", views.AvatarFormView.as_view(), name="change_avatar"),
    path("change_bio/", views.BioChangeFormView.as_view(), name="bio_change"),
    path("add_story/", views.AddStoryPage.as_view(), name="add_story_page"),
    path("add_story_form/", views.AddStoryFormView.as_view(), name="add_story_form"),
    path("feed_back/", views.FeedBackPageView.as_view(), name="feed_back_page"),
    path("feed_back_user/", views.FeedBackUserFormView.as_view(), name="feed_back_user"),
    path("feed_back_public/",views.FeedBackPublicFormView.as_view(), name="feed_back_public"),
    path("list_ranking_articles/", views.ArticleRankListView.as_view(), name="ranking_articles"),
    path("list_time_articles/", views.ArticleTimeListView.as_view(), name="time_list_articles"),
    path("list_ranking_articles/<str:topic>/", views.ArticleTopicTimeView.as_view(), name="article_topic_list"),
    path("articles/<int:author_id>/",views.ArticleAuthorTimeView.as_view(), name="authors_articles"),
    path("user/<int:author_id>/", views.AuthorPageView.as_view(), name="author_info")
]
