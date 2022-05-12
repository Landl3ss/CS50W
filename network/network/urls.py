
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post_entry/<str:sendto>", views.post_entry, name="post_entry"),
    path("page/<int:num>", views.page, name="page"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:user>/<int:num>", views.profile_page, name="profile_page"),
    path("following", views.following, name="following"),
    path("following/<int:num>", views.following_page, name="following_page"),
    path("<str:following>/to_follow", views.to_follow, name="to_follow"),
    path("edit_post/<int:postid>", views.edit_post, name="edit_post"),
    path("likeit/<int:postid>", views.likeit, name="likeit")
]
