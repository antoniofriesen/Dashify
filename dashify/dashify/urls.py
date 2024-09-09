from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboad"),
    path("users/", include("users.urls")),
    path("register/", include("users.urls")),
    path("logout/", include("users.urls")),
    path("plot/", include("plot.urls"))
]
