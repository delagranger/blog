from rest_framework import serializers
from blog.models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    char_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "body", "creation_date", "author", "tags", "char_count"]
        read_only_fields = ["id", "creation_date", "char_count"]

    def get_char_count(self, obj):
        return len(obj.body)