from dataclasses import field
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        field = "__all__"
        exclude = ["post"]
        labels = {
            "user_name" : "Your name",
            "user_email" : "Your Email",
            "comment_text": "Comment"
        }
