from django.contrib.auth import get_user_model
from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator

from posts.models import Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post
