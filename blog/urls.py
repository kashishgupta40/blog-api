from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, RegisterView, LoginView

router = DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blog')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
