from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .serializers import UserSerializer
from rest_framework import status
from datetime import datetime
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from wand.image import Image
from wand.display import display
import io
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def get_routes(request):
    routes = [
        {
            'Endpoint': '/posts/',
            'method': 'GET',
            'body': None,
            'description': 'Returns array of posts'
        }
    ]
    return Response(routes, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request):
    # user = request.user
    # posts = user.post_set.all()
    posts = Post.objects.all().order_by('-date')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_post(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        serializer = CommentSerializer(
            data={'comment': request.data['comment'], 'user': request.user.id, 'c_post': post.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response('Invalid request')
    elif request.method == 'GET':
        try:
            post = Post.objects.get(id=id)

            comments = post.c_post.all()
            comment_serializer = CommentSerializer(
                instance=comments, many=True)
        except Post.DoesNotExist:
            post = None
            return Response('Invalid request', status=status.HTTP_400_BAD_REQUEST)

        post_serializer = PostSerializer(post, many=False)
        return Response({'post': post_serializer.data, 'comments': comment_serializer.data}, status=status.HTTP_200_OK)


'''
@api_view(['DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def comment_adjustment(request, id):
    comment = Comment.objects.get(id=id)
    if request.method == 'PUT':
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response('Invalid request', status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        comment.delete()
        return Response('Comment deleted', status=status.HTTP_200_OK)
'''


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    request.data['user'] = request.user.id
    # request.data['date'] = datetime.now()
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
        return Response('Invalid request', status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        # print(f'serializer is not valid: {request.data}')
        if len(request.data['password']) > 8:
            return Response('Username or Email are already used, please choose a new one.', status=status.HTTP_400_BAD_REQUEST)
        elif len(request.data['password']) <= 8:
            return Response('Please, choose stronger password.', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Unknown issue', status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    return Response(f'user {request.user} deleted', status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, id):
    img_io = io.BytesIO()
    image = request.FILES['image']
    #print(image.size, image.name, image.file,
    #      image.content_type, image.field_name)
    #img_file = InMemoryUploadedFile(
    #    image.file,
    #    'image',
    #    image.name,
    #    image.content_type,
    #    image.size,
    #    None)
    if image.content_type == 'image/heif':
        img = Image(file=image)
        img.format = 'jpg'

        img.save(file=img_io)

        filename = image.name.replace('.heic', '.jpg')
        content_type = image.content_type.replace('heif', 'jpeg')
        img.save(filename=filename)
        img_file = InMemoryUploadedFile(
                img_io,
                'image',
                filename,
                content_type,
                sys.getsizeof(img_io),
                None)

        print(img_file.size, img_file.name, img_file.file,
              img_file.content_type, img_file.field_name)

        image = img_file
        #request.data['image'] = img_file
        #request.FILES['image'] = img_file

    #  data = request.data
    # print(img_file, image)

    loggedin_user = request.user.username
    post = Post.objects.get(id=id)

    post_user = post.user
    if (str(post_user) == str(loggedin_user)):
        serializer = PostSerializer(
            instance=post, data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
        else:
            print(serializer.errors)

        return Response(status=status.HTTP_200_OK)
    else:
        return Response('nene', status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, id):
    loggedin_user = request.user.username
    post = Post.objects.get(id=id)
    post_user = post.user
    if str(loggedin_user) == str(post_user):
        post_id = post.id
        post.delete()
        return Response(f'post {post_id} was deleted', status=status.HTTP_200_OK)
    else:
        return Response('Invalid request', status=status.HTTP_400_BAD_REQUEST)
