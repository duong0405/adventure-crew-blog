from django.shortcuts import render

# Create your views here.


def starting_page(request):
    return render(request, "blog/index.html")


def posts(request):
    pass


def post_detail(request):
    return render(request, "blog/post_detail.html")


def user_profile(request):
    return render(request, "blog/user_profile.html")
