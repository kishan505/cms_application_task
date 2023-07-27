from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Post, Like, Profile
import re
import json

# Create your views here.
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


class SignUpView(APIView):

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate required fields
        if not username or not email or not password:
            return Response({'error': 'username, email and password are required field '}, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already exist.'}, status=400)

        # check email valid or not
        if not is_valid_email(email):
            return Response({'error': 'Please enter valid email.'}, status=400)

        # check length of password
        if len(password) < 6:
            return Response({'error': 'password must be 6 character'}, status=400)

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        return Response({
            'success': 'User created successfully.',
            'user_id': user.pk
            }, status=201)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # required all fields
        if not username or not password:
            return Response({'error': 'Please provide both username and password.'}, status=400)

        # check Authenticate user
        user = authenticate(request, username=username, password=password)
        # try:
        #     user = User.objects.get(username=username)
        # except User.DoesNotExist:
        #     return ResourceWarning({'message': 'Login failed. Invalid username.'}, status=401)

        # Check authentication user or not
        if user is None:
            return Response({'error': 'Invalid username or password.'}, status=401)

        # Log in the user
        login(request, user)

        # Get or create a token for the user
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'success': 'User logged in successfully.',
            'user_id': user.pk,
            'token': token.key
        }, status=200)


class CreatePostView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title', '')
        description = request.data.get('description', '')
        content = request.data.get('content', '')
        author_id = request.data.get('author_id', '')
        is_public_post = request.data.get('is_public_post', 'True')

        if not title or not description or not content or not author_id:
            return Response({'error': 'Missing required fields.'}, status=400)

        if is_public_post not in ['True', 'true', 'False', 'false']:
            return Response({'error': 'Invalid input. Gives true or false value in is_public_post'}, status=400)

        try:
            author = User.objects.get(pk=author_id)
        except User.DoesNotExist:
            return Response({'error': 'Author does not exist.'}, status=404)

        post = Post(title=title, description=description, content=content, author=author, is_public_post=bool(is_public_post))
        post.save()

        return Response({'success': 'Post created successfully.'}, status=201)

class UpdatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        post_id = request.data.get('post_id')

        if not post_id:
            return Response({'error': 'Missing post_id fields.'}, status=400)

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist.'}, status=404)

        # Check if the authenticated user is the author of the post
        if post.author != request.user:
            return Response({'error': 'You are not allowed to update this post.'}, status=403)

        title = request.data.get('title', '')
        description = request.data.get('description', '')
        content = request.data.get('content', '')
        is_public_post = request.data.get('is_public_post', '')

        if is_public_post and is_public_post not in ['True', 'true', 'False', 'false']:
            return Response({'error': 'Invalid input. Gives true or false value in is_public_post'}, status=400)
        
        if title: post.title = title
        if description: post.description = description
        if content: post.content = content
        if is_public_post: post.is_public_post = bool(is_public_post)

        post.save()

        return Response({'success': 'Post updated successfully.'}, status=200)

class DeletePostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        post_id = request.data.get('post_id')

        if not post_id:
            return Response({'error': 'Missing post_id fields.'}, status=400)

        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist.'}, status=404)

        if post.author != request.user:
            return Response({"error": "You are not allowed to delete this post."}, status=403)

        post.delete()
        return Response({"message": "Post deleted successfully."}, status=204)

class GetPostById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        post_id = request.data.get('post_id')

        if not post_id:
            return Response({'error': 'Missing post_id fields.'}, status=400)
        
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist.'}, status=404)

        if post.author != request.user and post.is_public_post == False:
            return Response({"error": "You are not allowed to get this post."}, status=403)
        
        post_like_count = Like.objects.filter(post=post).count()
        post_data = {
                "post_id": post.post_id, 
                "title": post.title, 
                "content": post.content,
                "is_public_post": post.is_public_post,
                "likes": post_like_count
            }
        
        return Response(post_data, status=200)
        
class UserAllPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        posts = Post.objects.filter(author=user)

        if not posts.exists():
            return Response({"message": "User does not have any posts."}, status=404)
        
        posts_data = []
        for post in posts:

            post_like_count = Like.objects.filter(post=post).count()

            posts_data.append({
                "post_id": post.post_id, 
                "title": post.title, 
                "content": post.content,
                "is_public_post": post.is_public_post,
                "likes": post_like_count
            })
        return Response({"data": posts_data}, status=200)

class GetAllPostsView(APIView):

    def get(self, request):
        posts =  Post.objects.all()

        data = []
        for post in posts:
            if post.is_public_post == True:

                post_like_count = Like.objects.filter(post=post).count()
                data.append({
                    "post_id": post.post_id, 
                    "title": post.title, 
                    "content": post.content,
                    "is_public_post": post.is_public_post,
                    "likes": post_like_count
                })
        
        return Response({"data": data}, status=200)


class PostLikeDisLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_id = request.data.get('post_id')

        user = request.user

        # Get the blog post based on the post_id
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist.'}, status=404)

        # Check if the user has already liked the post
        if Like.objects.filter(user=user, post=post).exists():
            like = Like.objects.get(user=user, post=post)
            like.delete()

            return Response({"message": "Post dislike successfully."}, status=204)
        
        else:
            # Create a new like for the post
            Like.objects.create(user=user, post=post)
            return Response({"message": "Post liked successfully."}, status=201)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):

        email = request.data.get('email', '')
        mobile_no = request.data.get('mobile_no', '')
        city = request.data.get('city', '')
        country = request.data.get('country', '')

        try:
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=404)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile does not exist.'}, status=404)

        if email and not is_valid_email(email):
            return Response({'error': 'Please enter valid email.'}, status=400)
        
        if email: user.email = email
        if mobile_no: profile.mobile_no = mobile_no
        if city: profile.city = city
        if country: profile.country = country

        user.save()
        profile.save()

        return Response({'success': 'Profile updated successfully.'}, status=200)

class DeleteProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=404)
        
        if request.user.id != int(user_id):
            return Response({"message": "You are not allowed to delete this profile."}, status=403)

        user.delete()
        return Response({"message": "User deleted successfully."}, status=204)

