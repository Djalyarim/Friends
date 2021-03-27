from django import forms
from django.forms import Textarea

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')

<<<<<<< HEAD

=======
>>>>>>> 60bbec9238e8b566653de0fdb1132a9f88c60c0e
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 5}),
        }
<<<<<<< HEAD
=======

>>>>>>> 60bbec9238e8b566653de0fdb1132a9f88c60c0e
