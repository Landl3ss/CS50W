from tkinter import Widget
from django.db import models
from django.forms import Textarea

# Create your models here.

# class Languages(models.Model):
#     computer_ref = models.CharField(min_length=1, unique=True)
#     human_ref = models.CharField(min_length=1, unique=True)
    

# class Code(models.Model):
#     code = models.CharField(widget=Textarea, min_length=1)
#     code_type = models.CharField(choices=models.ForeignKey(Languages.computer_ref))
#     code_name = models.CharField(unique=True, min_length=5)
#     description = models.CharField(widget=Textarea)
