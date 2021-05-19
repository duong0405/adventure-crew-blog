from django.urls import path
from . import views

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("user", views.user_profile, name="user-profile"),
    path("posts/<slug:slug>", views.post_detail, name="post-detail-page"),

]
