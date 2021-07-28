from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from .form import UserRegistrationForm, UserProfileForm, UserProfileFormExtend, PostForm, ContentForm
from .models import Post, UserProfile, Tag
from django.utils.text import slugify
from django.views.generic import View, TemplateView, DetailView


# Create your views here.
class StartingPageView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lastest_posts = Post.objects.all().order_by("-date")[:3]
        context["posts"] = lastest_posts

        rating_posts = Post.objects.all().order_by("-rating")[:2]
        context["rating"] = rating_posts

        tags = Tag.objects.all()
        context["tags"] = tags

        return context
    
class PostDetailView(DetailView):
    template_name = "blog/post_detail.html"
    model = Post
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.author
        return context
    
class UserProfileView(View):

    def get_user_profile(self, username):
        users = UserProfile.objects.all()
        for user in users:
            if user.__str__() == username:
                return user
        return None
    
    def get_user_tags(self, posts):
        list_tags = []
        tags = {}
        for post in posts:
            list_tags += post.tags.all()
        for i in list_tags:
            tags[i] = list_tags.count(i)
        return tags

    def get(self, request, username):
        userprofile_form = UserProfileForm()
        userprofile_extendform = UserProfileFormExtend()

        user_profile = self.get_user_profile(username)
        if request.user.is_authenticated:
            userprofile_form = UserProfileForm(initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email
            })

        posts = Post.objects.filter(author=user_profile)
        tags = self.get_user_tags(posts)
        return render(request, "blog/user_profile.html", {
            "profile": user_profile,
            "userprofile_form": userprofile_form,
            "userprofile_extendform": userprofile_extendform,
            "posts": posts,
            "tags": tags
        })

    def post(self, request):
        existing_profile = UserProfile.objects.get(user__username=request.user.username)
        userprofile_form = UserProfileForm(request.POST, instance=existing_profile.user)
        userprofile_extendform = UserProfileFormExtend(
            request.POST, request.FILES, instance=existing_profile)

        if userprofile_extendform.is_valid() and userprofile_form.is_valid():
            userprofile_form.save()
            userprofile_extendform.save()
        return redirect("user-profile", existing_profile)

class UserLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "blog/login.html")

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            auth_user = authenticate(username=username, password=password)

            if auth_user is not None:
                login(request, auth_user)
                user_profile = UserProfile.objects.get(user__username=username)
                return redirect("user-profile", user_profile)
        return render(request, "blog/login.html", {
            "errors": form.errors.values()
        })

class UserRegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "blog/register.html")
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
        return render(request, "blog/register.html", {
         "errors": form.errors.values()
     })
    
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")

class CreatePostView(View):
    def get(self, request, username):
        post_form = PostForm()
        content_form = ContentForm()
        identified_user = UserProfile.objects.get(user__username=request.user.username)

        return render(request, "blog/create_post.html", {
            "profile": identified_user,
            "post_form": post_form,
            "content_form": content_form
        })
    
    def post(self, request):
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

        return render(request, "blog/create_post.html", {
            "profile": identified_user,
            "post_form": post_form,
            "content_form": content_form
        })
