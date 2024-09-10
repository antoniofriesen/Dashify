from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.
def posts_list(request):
    posts = Post.objects.all().order_by("-date")
    return render(request, "posts/posts_list.html", { "posts": posts })

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, "posts/post_page.html", { "post": post })

@login_required(login_url="users/login/")
def post_new(request):
    if request.method == "POST":
        form_new = forms.CreatePost(request.POST, request.FILES)
        if form_new.is_valid():
            newpost = form_new.save(commit=False)
            newpost.author =request.user
            newpost.save()
            return redirect("dashboard")
    else:
        form_new = forms.CreatePost()
    return render(request, "posts/post_new.html", { "form" : form_new })