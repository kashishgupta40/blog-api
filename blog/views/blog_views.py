from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from .models import Blog, Like
from .serializers import BlogSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import StandardResultsSetPagination

class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return (
            Blog.objects.select_related('author')
            .annotate(
                likes_count=Count('likes', distinct=True),
                comments_count=Count('comments', distinct=True),
            )
            .order_by('-created_at')
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def permission_denied(self, request, message=None, code=None):
        message = message or "You do not have permission to modify this blog."
        super().permission_denied(request, message=message, code=code)

    @swagger_auto_schema(request_body=BlogSerializer, responses={201: BlogSerializer})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(request_body=BlogSerializer, responses={200: BlogSerializer})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: 'No Content'})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(responses={201: 'Liked', 400: 'Already liked'})
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        blog = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, blog=blog)
        if not created:
            return Response({'detail': 'You have already liked this blog.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Blog liked successfully.'}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: 'Unliked', 400: "You haven't liked this blog yet"})
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        blog = self.get_object()
        like = Like.objects.filter(user=request.user, blog=blog).first()
        if like:
            like.delete()
            return Response({'detail': 'Blog unliked successfully.'}, status=status.HTTP_200_OK)
        return Response({'detail': "You haven't liked this blog yet."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CommentSerializer, responses={201: CommentSerializer})
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='comments')
    def add_comment(self, request, pk=None):
        blog = get_object_or_404(Blog, pk=pk)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, blog=blog)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: CommentSerializer(many=True)})
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly], url_path='comments')
    def list_comments(self, request, pk=None):
        blog = get_object_or_404(Blog, pk=pk)
        comments_qs = blog.comments.all().order_by('-created_at')
        page = self.paginate_queryset(comments_qs)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments_qs, many=True)
        return Response(serializer.data)