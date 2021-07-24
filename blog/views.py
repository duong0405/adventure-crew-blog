from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.forms import AuthenticationForm

from .form import UserRegistrationForm, UserProfileForm, UserProfileFormExtend, PostForm, ContentForm
from .models import Post, UserProfile
from django.utils.text import slugify

# Create your views here.


def starting_page(request):

    # Render 3 latest posts on starting page
    lastest_posts = Post.objects.all().order_by("-date")[:3]

    # Render 2 rating posts on starting page
    rating_posts = Post.objects.all().order_by("-rating")[:2]

    # Render tags
    tags = []
    unique_list = []
    for post in lastest_posts:
        tags += post.tags.all()
    for x in tags:
        if x not in unique_list:
            unique_list.append(x)

    return render(request, "blog/index.html", {
        "posts": lastest_posts,
        "rating": rating_posts,
        "tags": unique_list
    })


def post_detail(request, slug):
    identified_post = get_object_or_404(Post, slug=slug)
    author = identified_post.author
    return render(request, "blog/post_detail.html", {
        "post": identified_post,
        "profile": author
    })


def user_profile(request, username):
    if request.method == "POST":
        existing_profile = UserProfile.objects.get(
            user__username=request.user.username)

        userprofile_form = UserProfileForm(
            request.POST, instance=existing_profile.user)

        userprofile_extendform = UserProfileFormExtend(
            request.POST, request.FILES, instance=existing_profile)

        if userprofile_extendform.is_valid() and userprofile_form.is_valid():
            userprofile_form.save()
            userprofile_extendform.save()

        return redirect("user-profile", existing_profile)

    else:
        userprofile_form = UserProfileForm()
        userprofile_extendform = UserProfileFormExtend()

    users = UserProfile.objects.all()
    for user in users:
        if user.__str__() == username:
            user_profile = user
    if request.user.is_authenticated:
        userprofile_form = UserProfileForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        })

    posts = Post.objects.filter(author=user_profile)

    list_tags = []
    tags = {}
    for post in posts:
        list_tags += post.tags.all()
    for i in list_tags:
        tags[i] = list_tags.count(i)

    print(tags.keys())

    return render(request, "blog/user_profile.html", {
        "profile": user_profile,
        "userprofile_form": userprofile_form,
        "userprofile_extendform": userprofile_extendform,
        "posts": posts,
        "tags": tags
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


def create_post(request, username):

    if request.method == "POST":
        post_form = PostForm(request.POST)
        content_form = ContentForm(request.POST, request.FILES)

        if post_form.is_valid() and content_form.is_valid():
            content = content_form.save()
            post = post_form.save(commit=False)
            post.content = content
            post.slug = slugify(post.title)

            author = UserProfile.objects.get(
                user__username=request.user.username)
            post.author = author
            post.save()
            post_form.save_m2m()
        return redirect("user-profile", author)

    else:
        post_form = PostForm()
        content_form = ContentForm()

    identified_user = UserProfile.objects.get(
        user__username=request.user.username)

    return render(request, "blog/create_post.html", {
        "profile": identified_user,
        "post_form": post_form,
        "content_form": content_form
    })
