from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from blog.models import Post
from blog.serializers import PostSerializer

@api_view(["GET"])
def get_posts_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def get_post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == "PATCH":
        serializer = PostSerializer(post, data=request.data, patrial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == "DELETE":
        post.delete()
        return Response(status=204)

