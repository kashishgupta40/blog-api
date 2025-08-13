from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .blog_views import BlogViewSet
from .auth_views import AuthViewSet

router = DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]