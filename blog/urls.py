from django.urls import path
from . import views

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("user/<str:username>", views.user_profile, name="user-profile"),
    path("posts/<slug:slug>/", views.post_detail, name="post-detail-page"),
    path("login", views.user_login, name="login"),
    path("register", views.user_register, name="register")
]
