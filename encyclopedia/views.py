from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import util
from django import forms
from django.urls import reverse
import markdown2


class NewEncy(forms.Form):
    title = forms.CharField(label="Title" )
    Contents = forms.CharField(widget=forms.Textarea)

# Create your views here.

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    if title in util.list_entries():
        content = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": content
        })
    else:
        return render(request, "encyclopedia/error0.html")


def search(request):
    entries = util.list_entries()
    find_entries = list()
    search_box = request.POST.get("q", "")

    if search_box in entries:
        return HttpResponseRedirect(f"{search_box}")

    for entry in entries:
        if search_box in entry:
            find_entries.append(entry)
        else:
            print(f"{find_entries}")

    if find_entries:
        return render(request, "encyclopedia/search.html", {
          "search_result": find_entries,
          "search": search_box
        })

    else:
        return render(request, "encyclopedia/search.html", {
            "no_result": f"No results for {search_box}"
        })


def create(request):
    if request.method == "POST":
        form = NewEncy(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["Contents"]

            if title in util.list_entries():
                return render(request, "encyclopedia/error.html")

            util.save_entry(title, content)
            return redirect("title", title)

        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })

    return render(request, "encyclopedia/create.html", {
        "form": NewEncy()
    })


def edit(request, title=""):

    if request.method == 'POST':
        form = NewEncy(request.POST)
        title = form['title']
        print(form.is_valid(),form.errors)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["Contents"]
            util.save_entry(title,content)
            return redirect("title",title)

        else:
            return render(request,"encyclopedia/edit.html", {
                "form":form
            })

    form = NewEncy(initial={
        'title':title,
        'Contents':util.get_entry(title)
    })
    return render(request,"encyclopedia/edit.html",{
        "form":form,
        "title":title
    })

def Randompage(request):
    title = util.random_entry()
    return redirect("title", title)
