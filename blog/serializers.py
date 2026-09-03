from rest_framework import serializers
from blog.models import Post, Comment, Tag


class CommentSerializer(serializers.ModelSerializer):
    post_title = serializers.ReadOnlyField(source="post.title")
    char_count = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = ["id", "post", "text", "author", "author_username", "creation_date", "char_count"]
        read_only_fields = ["id", "author", "author_username", "creation_date", "char_count"]

    def get_char_count(self, obj):
        return len(obj.text)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    char_count = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source="author.username")
    tag_names = serializers.StringRelatedField(source="tags", many=True, read_only=True)

    class Meta:
        model = Post
        comments = CommentSerializer(many=True, read_only=True)

        fields = [
            "id", "title", "body", "creation_date", "image",
            "author", "author_username", "tags", "tag_names", "char_count",
            "comments"
        ]
        read_only_fields = [
            "id", "creation_date", "char_count", "author", "author_username", 
            "tag_names", "comments"
        ]

    def get_char_count(self, obj):
        return len(obj.body)

    def create(self, validated_data):
        comments_data = validated_data.pop("comments", [])
        post = Post.objects.create(**validated_data)
        for comment_data in comments_data:
            Comment.objects.create(post=post, **comment_data)
        return post