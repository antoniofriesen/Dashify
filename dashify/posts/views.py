import logging
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Post

# Set up logging
logger = logging.getLogger(__name__)

def posts_list(request):
    """
    Display a list of all posts ordered by date in descending order.

    :param request: The HTTP request object.
    :return: Rendered posts list page or error page.
    """
    try:
        posts = Post.objects.all().order_by("-date")
        return render(request, "posts/posts_list.html", {"posts": posts})
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        return render(request, "posts/error.html", {"error_message": "An error occurred while retrieving the posts."})

def post_page(request, slug):
    """
    Display a specific post based on the given slug.

    :param request: The HTTP request object.
    :param slug: The slug of the post to retrieve.
    :return: Rendered post detail page or error page.
    """
    try:
        post = Post.objects.get(slug=slug)
        return render(request, "posts/post_page.html", {"post": post})
    except ObjectDoesNotExist:
        logger.warning(f"Post with slug '{slug}' not found.")
        raise Http404("The post you are looking for does not exist.")
    except Exception as e:
        logger.error(f"Error fetching post with slug '{slug}': {e}")
        return render(request, "posts/error.html", {"error_message": "An error occurred while retrieving the post."})

@login_required(login_url="users/login/")
def post_new(request):
    """
    Handle the creation of a new post. Only accessible to logged-in users.

    :param request: The HTTP request object.
    :return: Rendered new post form or redirect to dashboard upon successful creation.
    """
    try:
        if request.method == "POST":
            form_new = forms.CreatePost(request.POST, request.FILES)
            if form_new.is_valid():
                newpost = form_new.save(commit=False)
                newpost.author = request.user
                newpost.save()
                logger.info(f"New post created by {request.user.username}.")
                return redirect("dashboard")
        else:
            form_new = forms.CreatePost()

        return render(request, "posts/post_new.html", {"form": form_new})
    except Exception as e:
        logger.error(f"Error creating new post by {request.user.username}: {e}")
        return render(request, "posts/error.html", {"error_message": "An error occurred while creating the post."})
