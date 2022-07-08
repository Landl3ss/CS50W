from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse

from .models import CodeFile


# Create your views here.

# The Home page
def index(request):
    files = CodeFile.objects.all()
    return render(request, "codebank/index.html", {
        'files' : files,
        'home' : 'active'
    })


def file_redirect(request, filename):
    return HttpResponseRedirect(reverse('file_view', kwargs={'filename': filename}))


def file_view(request, filename):
    if request.method == "GET":
        with open(f"/Users/wnoland/CS50W/capstone/code/{filename}", 'r') as codefile:
            code = codefile.read()
        return render(request, "codebank/file.html", {
            'filename' : filename,
            'code' : code
            })
    if request.method == "POST":
        with open(f"/Users/wnoland/CS50W/capstone/code/{filename}", 'w') as rewrite:
            rewrite.write(request.POST['code'])
        return HttpResponseRedirect(reverse('file_view', kwargs={'filename': filename}))


# The Upload page
def upload(request):
    if request.method == "POST":
        # print(request.POST['manual_entry'])
        with open(f"/Users/wnoland/CS50W/capstone/code/{request.POST['upload_code_name']}.py", 'w') as f:
            f.write(request.POST['manual_entry'])
        file = CodeFile(filename=f"{request.POST['upload_code_name']}.py", description=request.POST['description'], language=request.POST['lang'])
        file.save()
    return render(request, "codebank/upload.html", {
        'upload' : 'active'
    })

# The Combining page
def combine(request):
    return render(request, "codebank/comebine.html")