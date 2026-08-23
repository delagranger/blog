from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from blog.models import Post

def main_page(request):
    posts = Post.objects.all()
    return render(request, "blog/main_page.html", {"posts": posts})


def get_about_info(request):
    if request.method == "GET":
        return HttpResponse("Easy blog on Django")
    else:
        return HttpResponseBadRequest("Incorrect request method")


def get_post_by_id(request, id):
    return HttpResponse(f"You`ve opened post {id}")
