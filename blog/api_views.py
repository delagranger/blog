from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from blog.models import Post, Comment
from blog.serializers import PostSerializer, CommentSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backend = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['creation_date', 'title']
    ordering = ['-creation_date']
    filterset_fields = ['creation_date']
    search_fields = ['title', 'body']

    @action(detail=False, methods=["get"])
    def get_recent_posts(self, request):
        recent_posts = Post.objects.order_by("-creation_date")[:5]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer