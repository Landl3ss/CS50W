from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("search", views.search, name="search")
]
