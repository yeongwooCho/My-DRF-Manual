# Serializers define the API representation.
from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Post, Comment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'like', 'category', ]


class PostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ['id', 'title', 'image', 'like', 'category', ]
        exclude = ['create_dt']  # create_dt 이외의 모든 필드


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['like', ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
