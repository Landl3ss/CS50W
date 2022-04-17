from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from random import randint
from markdown2 import Markdown

from . import util


class EditEntry(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'cols': 50, 'rows': 4}))


class NewEntry(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'size': 51}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'cols': 50, 'rows': 4}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def new_entry(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if util.get_entry(title) != None:
                print('error') # ========================================================================
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('index'))

    return render(request, "encyclopedia/new_entry.html", {
        'form' : NewEntry()
    })


def wiki(request, title):
    md = Markdown()
    if title == None or title == 'None':
        en = util.list_entries()
        d = en[randint(0, len(en) - 1)]
        return render(request, "encyclopedia/entry.html", {
        'title' : d,
        'data' : md.convert(util.get_entry(d))
    }) 

    if util.get_entry(title) == None:
        return render(request, 'encyclopedia/error_entry_404.html')
    
 
    return render(request, "encyclopedia/entry.html", {
        'title' : title,
        'data' : md.convert(util.get_entry(title))
    })


def edit(request, title):
    if request.method == "POST":
        form = EditEntry(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title=title, content=content)
            return HttpResponseRedirect(reverse('wiki', kwargs={'title': title}))

    return render(request, "encyclopedia/edit.html", {
        'form' : EditEntry({'content': util.get_entry(title)}),
        'title': title
        })


def search(request):
    form = request.GET
    content = form['q']
    potential = util.list_entries()
    potential_list = []
    for j in potential:
        if content.lower() in j.lower():
            potential_list.append(j)
        if content.lower() == j.lower():
            return render(request, "encyclopedia/entry.html", {
                'entry' : j.lower(),
                'data' : util.get_entry(j.lower())
            })
    if len(potential_list) == 0:
        return render(request, 'encyclopedia/unknowns.html', {
            'entries' : None
        })
    return render(request, 'encyclopedia/unknowns.html', {
        'entries' : potential_list
    })
    