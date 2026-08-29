from rest_framework import serializers
from blog.models import Post, Comment, Tag


class PostSerializer(serializers.ModelSerializer):
    char_count = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source="author.username")
    tag_names = serializers.StringRelatedField(source="tags", many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "title", "body", "creation_date", "image",
            "author", "author_username", "tags", "tag_names", "char_count",
        ]
        read_only_fields = [
            "id", "creation_date", "char_count", "author", "author_username", "tag_names",
        ]

    def get_char_count(self, obj):
        return len(obj.body)


class CommentSerializer(serializers.ModelSerializer):
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