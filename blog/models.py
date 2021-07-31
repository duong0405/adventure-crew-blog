from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="profile")
    avatar = models.ImageField(upload_to="users", default='users/avatar-default.jpg', null=True, blank=True)
    cover = models.ImageField(upload_to="users", default='users/cover-default.jpg', null=True, blank=True)
    member = models.CharField(max_length=30, default="Junior Member")
    articles = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)

    def full_name(self):
        if self.user.first_name == "" or self.user.last_name == "":
            return self.user.username
        else:
            return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.full_name()


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Content(models.Model):
    heading1 = models.CharField(max_length=100)
    paragraph1 = models.TextField(MinLengthValidator(10))
    image1 = models.ImageField(upload_to="posts", null=True, blank=True)

    heading2 = models.CharField(max_length=100)
    paragraph2 = models.TextField(MinLengthValidator(10))
    image2 = models.ImageField(upload_to="posts", null=True, blank=True)

    heading3 = models.CharField(blank=True, max_length=100)
    paragraph3 = models.TextField(blank=True)
    image3 = models.ImageField(upload_to="posts", null=True, blank=True)

    heading4 = models.CharField(blank=True, max_length=200)
    paragraph4 = models.TextField(blank=True)
    image4 = models.ImageField(upload_to="posts", null=True, blank=True)

    def __str__(self):
        return self.heading1


class Post(models.Model):
    class Format(models.IntegerChoices):
        FORMAT_1 = 1
        FORMAT_2 = 2
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    date = models.DateField()
    slug = models.SlugField(unique=True, db_index=True)
    post_format = models.IntegerField(choices=Format.choices)
    post_preview = models.TextField(MinLengthValidator(
        10), blank=False, null=True, default=None)
    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    author = models.ForeignKey(
        UserProfile, null=True, on_delete=models.SET_NULL, related_name="posts")
    tags = models.ManyToManyField(Tag)
    rating = models.FloatField(null=True, blank=True, default=None, validators=[
                               MinValueValidator(0.0), MaxValueValidator(10.0)])

    def __str__(self):
        return self.title

class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
