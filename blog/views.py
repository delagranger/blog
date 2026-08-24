from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import ListView, DetailView

from blog.models import Post
from blog.forms import CommentForm

class PostsList(ListView):
    model = Post
    template_name = "blog/main_page.html"
    context_object_name = "posts"


class PostInfo(DetailView):
    model = Post
    template_name = "blog/post_info.html"
    context_object_name = "post"


def get_about_info(request):
    if request.method == "GET":
        return HttpResponse("Easy blog on Django")
    else:
        return HttpResponseBadRequest("Incorrect request method")


def add_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main_page")
    else:
        form = CommentForm()

    return render(request, "blog/form.html", {"form": form})