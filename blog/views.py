from django.shortcuts import render
from datetime import datetime
from . import posts

# Create your views here.


def get_date(post):
    return post["date"]


def starting_page(request):

    # Render 3 latest posts on starting page
    sorted_posts = sorted(posts.all_posts, key=get_date)
    lastest_posts = sorted_posts[-3:]

    for post in lastest_posts:
        post['dateformat'] = post['date'].strftime('%B %d, %Y')

    return render(request, "blog/index.html", {
        "posts": lastest_posts
    })


def post_detail(request, slug):
    return render(request, "blog/post_detail.html")


def user_profile(request):
    return render(request, "blog/user_profile.html")
