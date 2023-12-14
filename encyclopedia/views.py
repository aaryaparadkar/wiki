from django.shortcuts import render
import markdown
import random
from . import util

def mdtohtml(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if(content == None):
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = mdtohtml(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = mdtohtml(entry_search)
        if html_content != None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            allentries = util.list_entries()
            rec = []
            for entry in allentries:
                if entry_search.lower() in entry.lower():
                    rec.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": rec
            })
        
def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else: 
        title = request.POST['title']
        content = request.POST['content']
        titleexists = util.get_entry(title)
        if titleexists != None:
            return render(request, "encyclopedia/error.html", {
                "message": "This title already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = mdtohtml(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })

def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = mdtohtml(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def random_entry(request):
    allentries = util.list_entries()
    num = len(allentries)
    randomnum = random.randint(0, num-1)
    title = allentries[randomnum]
    html_content = mdtohtml(title)
    return render(request, "encyclopedia/entry.html", {
        "title": randomnum,
        "content": html_content
    })

# def randoms(request):
#     entries = util.list_entries()
#     num = len(entries)
#     randomnum = random.randint(0, num-1)
#     title = entries[randomnum]
#     return render(request, "encyclopedia/entry.html", {"entry_name": title, "content": markdowner.convert(util.get_entry(title))})