from django.urls import path
from blog.api_views import get_posts_list, get_post_details

urlpatterns = [
    path("posts/", get_posts_list),
    path("post/<int:pk>/", get_post_details)
]