from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Function that handles new user's registration
def register_user(request):
    if request.method == "POST":
        form_register = UserCreationForm(request.POST)
        if form_register.is_valid():
            form_register.save()
            # TODO: dummy redirection: add path to login here
            return redirect("home")
    else:
        form_register = UserCreationForm()
    return render(request, "users/register.html", { "form": form_register })

# Function that handles user's login
def login_user(request):
    if request.method == "POST":
        form_login = AuthenticationForm(data=request.POST)
        if form_login.is_valid():
            user = form_login.get_user()
            login(request, user)
            # TODO: dummy redirection: add path to dashboard here
            return redirect("home")
    else:
        form_login = AuthenticationForm()
    return render(request, "users/login.html", { "form": form_login })

# Function that hangles the registration of new users
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")

