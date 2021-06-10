from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model

from .form import UserRegistrationForm
from django.contrib import messages
from .models import Post

# Create your views here.


def starting_page(request):

    # Render 3 latest posts on starting page
    lastest_posts = Post.objects.all().order_by("-date")[:3]

    # Render 2 rating posts on starting page
    rating_posts = Post.objects.all().order_by("-rating")[:2]

    # Render tags
    tags = []

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
        "user": author
    })


def user_profile(request, username):
    for user in users.users:
        if user['name'] == username:
            identified_user = user
    return render(request, "blog/user_profile.html", {
        "user": identified_user
    })


def user_login(request):
    return render(request, "blog/login.html")


def user_register(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    pw1 = request.POST.get("password1")
    pw2 = request.POST.get("password2")
    print(username, email, pw1, pw2)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        else:
            for error in list(form.errors.values()):
                messages.error(
                    request, "Unsuccessful registration. Invalid information.")
                print(request, error)
    else:
        form = UserRegistrationForm()
    return render(request, "blog/register.html", context={"form": form})
