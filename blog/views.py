from django.shortcuts import render
from datetime import datetime
from . import posts
from . import userposts
from . import users

# Create your views here.


def get_date(post):
    return post["date"]


def get_rate(post):
    return post['rate']


def starting_page(request):

    # Render 3 latest posts on starting page
    sorted_posts = sorted(posts.all_posts, key=get_date)
    lastest_posts = sorted_posts[-3:]

    # Render 2 rating posts on starting page
    sorted_rating_posts = sorted(posts.all_posts, key=get_rate)
    rating_posts = []

    for post in sorted_rating_posts[-2:]:
        for user_post in userposts.all_posts:
            if user_post['slug'] == post['slug']:
                rating_posts.append(user_post)

    # Render tags
    tags = []
    for post in lastest_posts:
        tags += post['tags']

    return render(request, "blog/index.html", {
        "posts": lastest_posts,
        "rating": rating_posts,
        "tags": tags
    })


def post_detail(request, slug):
    identified_post = next(
        post for post in userposts.all_posts if post['slug'] == slug)

    for user in users.users:
        if (user['name'] == identified_post['author']):
            identified_user = user

    return render(request, "blog/post_detail.html", {
        "post": identified_post,
        "user": identified_user
    })


def user_profile(request):
    return render(request, "blog/user_profile.html")
