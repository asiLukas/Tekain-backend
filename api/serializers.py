from rest_framework.serializers import ModelSerializer
from .models import Post, Comment
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.user:
            ret['author'] = {"id": instance.user.id,
                             "username": instance.user.username}
        return ret


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.user:
            ret['author'] = instance.user.username
        return ret


class UserSerializer(ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        required=True,
        max_length=20,
        min_length=2,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
