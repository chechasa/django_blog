from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name='starting_page'),
    path('posts/', views.Posts.as_view(), name='posts_page'),
    path('posts/<slug:slug>/', views.PostDetail.as_view(), name='post_detail_page'),
    path("read-later/", views.ReadLaterView.as_view(), name="read-later")
]
