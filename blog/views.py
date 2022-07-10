from calendar import c
from cgitb import html
from queue import Empty
from urllib import request
from webbrowser import get
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from datetime import date
from .models import Post, Comment
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from django.urls import reverse
from django.views import View


all_posts = Post.objects.all().order_by("-date")


class Index(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts" #"object_list" is the default if no value is given 

    def get_queryset(self):
        queryset = super().get_queryset()
        query = queryset[:3]
        return query

# def index(request):
#     latest_posts = all_posts[:3]
#     return render(request, 'blog/index.html', context={
#         'posts': latest_posts
#     }) 

class Posts(ListView):
    template_name = "blog/all_posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"

# def posts(request):
#     return render(request, 'blog/all_posts.html', context={
#         "all_posts": all_posts
#     })

# class PostDetail(DetailView):
#     template_name = "blog/post_detail.html"
#     model = Post

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tag.all()
#         context["comment_form"] = CommentForm()
#         return context
    
class PostDetail(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        is_comment_empty = True
        if not post.comments.all().exists():
            is_comment_empty = True
        else:
            is_comment_empty = False

        return render(request, "blog/post_detail.html", context={
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "is_saved_for_later": self.is_stored_post(request, post.id),
            "is_comment_empty": is_comment_empty
        })

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        # comments = Comment.objects.filter(post=post)

        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post_detail_page", args=[slug]))
        
        return render(request, "blog/post_detail.html", context={
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),

        })


# def post_detail(request, slug): 
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post_detail.html", context={
#         "post": identified_post
#     })


    #  sorted_posts = sorted(all_posts,key=get_date)
    # latest_posts = sorted_posts[-3:]
    # return render(request, 'blog/post_detail.html', context={
    #     'posts': latest_posts
    # }) 
    
class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
            
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored_posts.html", context)
    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:    
            stored_posts.append(int(request.POST["post_id"]))
        elif post_id in stored_posts:  
            stored_posts.remove(int(request.POST["post_id"]))
        
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")