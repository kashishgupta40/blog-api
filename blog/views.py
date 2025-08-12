from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema

from .models import Blog, Like, Comment
from .serializers import (
    BlogSerializer,
    CommentSerializer,
    RegisterSerializer,
    UserSerializer,
    LoginSerializer,  
)
from .permissions import IsOwnerOrReadOnly


class RegisterView(APIView):
    permission_classes = []
    serializer_class = RegisterSerializer 

    @swagger_auto_schema(request_body=RegisterSerializer, responses={201: UserSerializer})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response(
            {'token': token.key, 'user': UserSerializer(user).data},
            status=status.HTTP_201_CREATED
        )


class LoginView(ObtainAuthToken):
    permission_classes = []

    @swagger_auto_schema(request_body=LoginSerializer, responses={200: UserSerializer})
    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        token_key = res.data.get('token')
        token = Token.objects.get(key=token_key)
        return Response(
            {'token': token.key, 'user': UserSerializer(token.user).data}
        )


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Blog.objects.select_related('author').annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments')
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        blog = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, blog=blog)
        if not created:
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Liked'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        blog = self.get_object()
        try:
            like = Like.objects.get(user=request.user, blog=blog)
            like.delete()
            return Response({'detail': 'Unliked'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'detail': 'You have not liked this blog'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='comments')
    def add_comment(self, request, pk=None):
        blog = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, blog=blog)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly], url_path='comments')
    def list_comments(self, request, pk=None):
        blog = self.get_object()
        comments_qs = blog.comments.all().order_by('-created_at')
        page = self.paginate_queryset(comments_qs)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments_qs, many=True)
        return Response(serializer.data)
