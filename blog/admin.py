from django.contrib import admin
from blog.models import Tag, Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "creation_date")
    list_filter = ("creation_date",)
    search_fields = ("title",)
    search_help_text = ("Search by title")

class CommentAdmin(admin.ModelAdmin):
    list_filter = ("creation_date",)
    search_fields = ("author",)
    search_help_text = ("Search by author")


admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

