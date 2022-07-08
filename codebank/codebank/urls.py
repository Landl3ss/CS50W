from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("file_view/<str:filename>", views.file_view, name="file_view"),
    path("file_redirect/<str:filename>", views.file_redirect, name="file_redirect"),
    path("upload", views.upload, name="upload")
]