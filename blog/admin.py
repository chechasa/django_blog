from django.contrib import admin
from .models import Author, Post, Tag, Comment

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "tag", "date")
    list_display = ("title", "date", "author")
    prepopulated_fields = {"slug": ("title",)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user_name")
    list_filter = ("post", "user_name")
# Register your models here.
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
