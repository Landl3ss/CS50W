from django.shortcuts import render
from django.urls import reverse


# Create your views here.

def index(request):

    code = ""

    print(request.method)
    if request.method == "POST":
        
        print(request.POST['code'])

    return render(request, "codebank/index.html", {
        'code' : code
    })