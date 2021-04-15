from django import forms
from django.forms import Textarea

from .models import Comment, Post, Profile_id


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 5}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile_id
        fields = ('text_profile', 'image_author',)
