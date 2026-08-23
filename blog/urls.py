from django.urls import path
from blog import views

urlpatterns = [
    path("", views.main_page),
    path("post/<int:id>/", views.get_post_by_id),
    path("about/", views.get_about_info),
]