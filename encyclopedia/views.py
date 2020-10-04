from random import choice

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def show_entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            'message': 'This entry does not exist'
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown(entry)
    })


def search(request):
    query = request.GET['q'].lower()
    results = []
    for title in util.list_entries():
        if title.lower() == query:
            return HttpResponseRedirect(reverse('show_entry', kwargs={
                'title': title
            }))
        elif title.lower().__contains__(query):
            results.append(title)
    return render(request, 'encyclopedia/results.html', {
        'results': results
    })


def create_entry(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        if title not in util.list_entries():
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('show_entry', kwargs={
                'title': title
            }))
        else:
            return render(request, "encyclopedia/error.html", {
                'message': 'This entry already exists'
            })
    return render(request, "encyclopedia/create.html")


def edit_entry(request, title):
    entry = util.get_entry(title)
    if request.method == 'POST':
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('show_entry', kwargs={
                'title': title
            }))
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "entry": entry
    })


def random_entry(request):
    title = choice(util.list_entries())
    entry = util.get_entry(title)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown(entry)
    })

