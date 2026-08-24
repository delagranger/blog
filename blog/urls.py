from django.urls import path
from blog import views
from blog.views import PostsList, PostInfo

urlpatterns = [
    path("", PostsList.as_view(), name="list"),
    path("post/<int:pk>/", PostInfo.as_view(), name="post"),
    path("about/", views.get_about_info),
]