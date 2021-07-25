from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("user/<str:username>", views.user_profile, name="user-profile"),
    path("posts/<slug:slug>/", views.post_detail, name="post-detail-page"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("register", views.user_register, name="register"),
    path("user/<str:username>/create-new-post",
         views.create_post, name="create-post"),
]
