from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=24, default=None, unique=True)
    email = models.EmailField(max_length=20, default=None, unique=True)
    # following = []


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="author")
    text = models.TextField(default=None)
    time = models.DateTimeField(auto_now_add=True)
  
    def serialize(self, same):

        return {
            "id": self.id,
            "author": self.author.username,
            "text": self.text,
            "time": self.time.strftime("%b %d %Y, %I:%M %p"),
            "same": same
        }


class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="liker")
    the_post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name="the_post")
    liked = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "liker": self.liker.username,
            "the_post": self.the_post,
            "liked": self.liked
        }


class Follows(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="person")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="shadow")
    isfollowing = models.BooleanField(default=False)

# class Comment(models.Model):
#     commenter = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="commenter")
#     topic = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name="topic")
#     text = models.TextField(default=None)

#     def serialize(self):
#         return {
#             "id": self.id,
#             "commenter": self.commenter.username,
#             "topic": self.topic,
#             "text": self.text
#         }