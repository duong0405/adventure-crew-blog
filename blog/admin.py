from django.contrib import admin
from .models import UserProfile, Tag, Content, Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "tags", "date")
    list_display = ("title", "date", "author")
    prepopulated_fields = {"slug": ("title",)}


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Content)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
