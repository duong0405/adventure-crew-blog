from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.forms import AuthenticationForm

from .form import UserRegistrationForm
from .models import Post, UserProfile
from django.contrib import messages

# Create your views here.


def starting_page(request):

    # Render 3 latest posts on starting page
    lastest_posts = Post.objects.all().order_by("-date")[:3]

    # Render 2 rating posts on starting page
    rating_posts = Post.objects.all().order_by("-rating")[:2]

    # Render tags
    tags = []
    for post in lastest_posts:
        tags += post.tags.all()

    return render(request, "blog/index.html", {
        "posts": lastest_posts,
        "rating": rating_posts,
        "tags": tags
    })


def post_detail(request, slug):
    identified_post = get_object_or_404(Post, slug=slug)
    author = identified_post.author
    return render(request, "blog/post_detail.html", {
        "post": identified_post,
        "profile": author
    })


def user_profile(request, username):
    users = UserProfile.objects.all()
    for user in users:
        if user.__str__() == username:
            user_profile = user

    return render(request, "blog/user_profile.html", {
        "profile": user_profile,
    })


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            auth_user = authenticate(username=username, password=password)

            if auth_user is not None:
                login(request, auth_user)
                user_profile = UserProfile.objects.get(user__username=username)
                return redirect("user-profile", user_profile)
    else:
        form = AuthenticationForm()

    return render(request, "blog/login.html", {
        "errors": form.errors.values()
    })


def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserRegistrationForm()

    return render(request, "blog/register.html", {
        "errors": form.errors.values()
    })


def user_logout(request):
    logout(request)
    return redirect("/")
