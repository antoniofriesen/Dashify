from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def dashboard(request):
    return render(request, "dashboard.html")

def plots(request):
    return render(request, "plot.html")

def todos(request):
    return render(request, "todos.html")

def blog(request):
    return render(request, "blog.html")
