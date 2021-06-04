from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(upload_to='images')
    cover = models.ImageField(upload_to='images')
    member = models.CharField(max_length=30)
    articles = models.IntegerField()
    followers = models.IntegerField()
    rating = models.FloatField()

    def __str__(self):
        return self.user.username
