from django.urls import path
from blog.api_views import PostsListAPIView, PostAPIView

urlpatterns = [
    path("posts/", PostsListAPIView.as_view()),
    path("post/<int:pk>/", PostAPIView.as_view())
]