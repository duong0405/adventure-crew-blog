from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Post, Tag, Content


class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        profile = UserProfile(user=user)
        if commit:
            user.save()
            profile.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class UserProfileFormExtend(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ("avatar", "cover")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "excerpt", "post_format", "post_preview")
        labels = {
            "title": "Title",
            "excerpt": "Excerpt",
            "post_format": "Format",
            "post_preview": "Post Preview"
        }
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control'}),
            'post_format': forms.Select(attrs={'class': 'form-control'}),
            'post_preview': forms.Textarea(attrs={'class': 'form-control'})
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("tags",)
        widgets = {
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ("heading1", "paragraph1", "image1", "heading2", "paragraph2", "image2",
                  "heading3", "paragraph3", "image3",
                  "heading4", "paragraph4", "image4")
        labels = {
            "heading1": "Heading 1",
            "heading2": "Heading 2",
            "heading3": "Heading 3",
            "heading4": "Heading 4",
            "paragraph1": "Paragraph 1",
            "paragraph2": "Paragraph 2",
            "paragraph3": "Paragraph 3",
            "paragraph4": "Paragraph 4",
        }

        widgets = {
            'heading1': forms.TextInput(attrs={'class': 'form-control'}),
            'paragraph1': forms.Textarea(attrs={'class': 'form-control'}),

            'heading2': forms.TextInput(attrs={'class': 'form-control'}),
            'paragraph2': forms.Textarea(attrs={'class': 'form-control'}),

            'heading3': forms.TextInput(attrs={'class': 'form-control'}),
            'paragraph3': forms.Textarea(attrs={'class': 'form-control'}),

            'heading4': forms.TextInput(attrs={'class': 'form-control'}),
            'paragraph4': forms.Textarea(attrs={'class': 'form-control'}),
        }
