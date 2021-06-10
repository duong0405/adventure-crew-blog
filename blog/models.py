from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.CharField(max_length=100)
    cover = models.CharField(max_length=100)
    member = models.CharField(max_length=30)
    articles = models.IntegerField()
    followers = models.IntegerField()
    rating = models.FloatField()

    def full_name(self):
        if not self.user.first_name and not self.user.last_name:
            return f"{self.user.first_name} { self.user.last_name}"
        return self.user.username

    def __str__(self):
        return self.full_name()


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Content(models.Model):
    heading1 = models.CharField(max_length=200)
    paragraph1 = models.TextField(MinLengthValidator(10))
    img1 = models.CharField(max_length=100)

    heading2 = models.CharField(max_length=200)
    paragraph2 = models.TextField(MinLengthValidator(10))
    img2 = models.CharField(max_length=100)

    heading3 = models.CharField(blank=True, max_length=200)
    paragraph3 = models.TextField(blank=True)
    img3 = models.CharField(blank=True, max_length=100)

    heading4 = models.CharField(blank=True, max_length=200)
    paragraph4 = models.TextField(blank=True)
    img4 = models.CharField(blank=True, max_length=100)


class Post(models.Model):
    class Format(models.IntegerChoices):
        FORMAT_1 = 1
        FORMAT_2 = 2
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)
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
