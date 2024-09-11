import logging
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Set up logging
logger = logging.getLogger(__name__)

# Function that handles new user's registration
def register_user(request):
    """
    Handles new user registration using the built-in UserCreationForm.

    :param request: The HTTP request object.
    :return: Rendered registration page or redirect to home upon successful registration.
    """
    try:
        if request.method == "POST":
            form_register = UserCreationForm(request.POST)
            if form_register.is_valid():
                form_register.save()
                logger.info("New user registered successfully.")
                return redirect("home")
        else:
            form_register = UserCreationForm()

        return render(request, "users/register.html", {"form": form_register})
    
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        return render(request, "users/error.html", {"error_message": "An error occurred during registration."})

# Function that handles user's login
def login_user(request):
    """
    Handles user login using the built-in AuthenticationForm.

    :param request: The HTTP request object.
    :return: Rendered login page or redirect to dashboard upon successful login.
    """
    try:
        if request.method == "POST":
            form_login = AuthenticationForm(data=request.POST)
            if form_login.is_valid():
                user = form_login.get_user()
                login(request, user)
                logger.info(f"User {user.username} logged in successfully.")
                return redirect("dashboard")
        else:
            form_login = AuthenticationForm()

        return render(request, "users/login.html", {"form": form_login})
    
    except Exception as e:
        logger.error(f"Error during user login: {e}")
        return render(request, "users/error.html", {"error_message": "An error occurred during login."})

# Function that handles user's logout
def logout_user(request):
    """
    Logs the user out and redirects to the home page.

    :param request: The HTTP request object.
    :return: Redirect to home upon logout.
    """
    try:
        if request.method == "POST":
            logout(request)
            logger.info("User logged out successfully.")
            return redirect("home")
    
    except Exception as e:
        logger.error(f"Error during user logout: {e}")
        return render(request, "users/error.html", {"error_message": "An error occurred during logout."})
