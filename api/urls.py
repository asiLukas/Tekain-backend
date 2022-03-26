from django.urls import path
from .views import get_routes, get_posts, get_post, create_post, update_post, delete_post, MyTokenObtainPairView, create_user, delete_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', get_routes, name='routes'),
    path('p/', get_posts, name='posts'),
    path('p/<str:id>/u/', update_post, name='update-post'),
    path('p/<str:id>/d/', delete_post, name='delete-post'),
    path('p/n/', create_post, name='create-post'),
    path('p/<str:id>/', get_post, name='post'),
    path('user/register/', create_user, name='register-user'),
    path('user/delete/', delete_user, name='delete-user'),
    #path('comment/<str:id>/adjust/', comment_adjustment, name='adjust-comment'),
]
