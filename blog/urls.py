from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("user/<str:username>", views.user_profile, name="user-profile"),
    path("posts/<slug:slug>/", views.post_detail, name="post-detail-page"),
    path("login", views.UserLoginView.as_view(), name="login"),
    path("logout", views.UserLogoutView.as_view(), name="logout"),
    path("register", views.UserRegisterView.as_view(), name="register"),
    path("user/<str:username>/create-new-post",
         views.create_post, name="create-post"),
]
