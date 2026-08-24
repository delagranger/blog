from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from blog.models import Post
from blog.forms import CommentForm


class PostsList(ListView):
    model = Post
    template_name = "blog/main_page.html"
    context_object_name = "posts"


class PostInfo(LoginRequiredMixin, DetailView):
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


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})