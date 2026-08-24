from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from blog.models import Post, Comment
from blog.serializers import PostSerializer, CommentSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=["get"])
    def get_recent_posts(self, request):
        recent_posts = Post.objects.order_by("-creation_date")[:5]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



