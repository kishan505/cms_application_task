from django.urls import path
from .views import (
    SignUpView, LoginView, 
    GetAllPostsView, CreatePostView, UpdatePostView, DeletePostView,
    PostLikeDisLikeView, UserAllPostsView, GetPostById, UpdateProfileView,
    DeleteProfileView
    
)

urlpatterns = [
    path('sign_up', SignUpView.as_view(), name="sign_up"),
    path('login', LoginView.as_view(), name="login"),

    path('create_post', CreatePostView.as_view(), name="create_post"),
    path('update_post', UpdatePostView.as_view(), name="update_post"),
    path('delete_post', DeletePostView.as_view(), name="delete_post"),
    path('get_post_by_id', GetPostById.as_view(), name="get_post_by_id"),
    path('user_all_posts', UserAllPostsView.as_view(), name="user_all_posts"),
    path('get_all_posts', GetAllPostsView.as_view(), name="get_all_posts"),

    path('post_like_dislike', PostLikeDisLikeView.as_view(), name="post_like_dislike"),

    path('update_profile', UpdateProfileView.as_view(), name="update_profile"),
    path('delete_profile', DeleteProfileView.as_view(), name="delete_profile"),
]
