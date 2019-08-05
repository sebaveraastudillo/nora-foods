from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create-menu/", views.createMenu, name="createMenu"),
    path("create-option/", views.createOption, name="createOption")
]