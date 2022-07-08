from tkinter.tix import INTEGER
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.


fs = FileSystemStorage(location='/Users/wnoland/CS50W/capstone/code/')

class CodeFile(models.Model):

    class PROGRAMMING_LANGUAGES(models.TextChoices):
        PYTHON = 'py', _('PYTHON')
        C = 'c', _('C')
        CPP = 'cpp', _('C++')
        CSHP = 'cshp', _('C#')
        R = 'r', _('R')
        HTML = 'html', _('HTML')
        CSS = 'css', _('CSS')
        JS = 'js', _('JAVASCRIPT')
        JULIA = 'juli', _('JULIA')

    class OUTPUTS(models.TextChoices):
        DICTIONARY = 'dict', _('DICTIONARY')
        ARRAY = 'list', _('ARRAY')
        BOOLEAN = 'bool', _('BOOLEAN')
        INTEGER = 'int', _('INTEGER')
        FLOAT = 'float', _('FLOAT')
        STRING = 'str', _('STRING')

    filename = models.CharField(unique=True, max_length=50)
    # file = models.FileField(max_length=200, upload_to='code/', storage=fs)
    filepath = models.FilePathField(path='/Users/wnoland/CS50W/capstone/code/')
    description = models.TextField()
    language = models.CharField(choices=PROGRAMMING_LANGUAGES.choices, max_length=4)
    inputs = models.IntegerField(default=1)
    output = models.CharField(choices=OUTPUTS.choices, max_length=10, default=INTEGER)
