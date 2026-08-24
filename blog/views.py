from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest

from blog.models import Post
from blog.forms import CommentForm

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


def add_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main_page")
    else:
        form = CommentForm()

    return render(request, "blog/form.html", {"form": form})