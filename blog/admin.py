from django.contrib import admin
from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "creation_date")
    list_filter = ("creation_date",)
    search_fields = ("title",)
    search_help_text = ("Search by title")

admin.site.register(Post, PostAdmin)

