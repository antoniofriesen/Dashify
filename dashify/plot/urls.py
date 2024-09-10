from django.urls import path
from . import views

app_name = "plot"

urlpatterns = [
    path("plot/", views.plot, name="plot"),
    path("darstellungen/",views.main, name="darstellungen")
]
