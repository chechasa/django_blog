from distutils.command.upload import upload
from tkinter import CASCADE
from django.db import models
from django.forms import CharField, SlugField
from django.utils.text import slugify
from django.urls import reverse
from datetime import date

# Create your models here.
class Tag(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self):
        return self.caption

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    title = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(null=False, default="", db_index=True, blank=True, max_length=100, unique=True)
    image = models.ImageField(upload_to="images", name="image")
    content = models.TextField()
    excerpt = models.TextField()
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.SET_DEFAULT, null=True, default=0, related_name="posts")
    tag = models.ManyToManyField(Tag)

    
    def __str__(self):
        return f"{self.title} | {self.author.first_name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField(null=True)
    comment_text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", null=True)