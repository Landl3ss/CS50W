from tkinter import Widget
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=25, unique=True)
    password = models.CharField(max_length=25)
    watchlist = []

class Listings(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='seller')
    item = models.CharField(max_length=64, default=None)
    description = models.TextField(default=None)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    image = models.URLField(null=True, default=None)
    active = True
    category = []

class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, default=None)

class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    comment = models.TextField(default=None)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, default=None)