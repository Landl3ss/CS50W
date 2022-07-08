from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("get_price", views.get_price, name="get_price")
]