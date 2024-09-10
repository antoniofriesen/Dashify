from django.urls import path
from . import views

app_name = "plot"

urlpatterns = [
    path("plot/", views.main, name="plot")

]
