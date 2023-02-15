from django.shortcuts import render
from django.http import HttpResponseNotFound
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html", {
            "error": 404
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": util.get_entry(title)
    })
    
def search(request):
    if request.method == "POST":
        q = request.POST.get("q")
        if not q:
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            })
        elif q.lower() in [x.lower() for x in util.list_entries()]:
            # Finding the index of the entry in list_entries
            # This allows to refer to the original title without many operations on "q" query from the HTML form
            index = [x.lower() for x in util.list_entries()].index(q.lower())
            
            return render(request, "encyclopedia/entry.html", {
                "title": util.list_entries()[index],
                "content": util.get_entry(q)
            })
        else:
            result_list = []
            for i in range(len(util.list_entries())):
                if q.lower() in util.list_entries()[i].lower():
                    result_list.append(util.list_entries()[i])    
            print(result_list)
            return render(request, "encyclopedia/search.html", {
                    "query": q,
                    "result_list": result_list
            })
            
def newpage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if not title:
            return render(request, "encyclopedia/error.html", {
                "error": "No title provided"
            })
        elif title.lower() in [x.lower() for x in util.list_entries()]:
            return render(request, "encyclopedia/error.html", {
                "error": "Such article already exists"
            })
            
        newcontent = request.POST.get("newcontent")
        if not newcontent:
            return render(request, "encyclopedia/error.html", {
                "error": "Please provide the content"
            })
        util.save_entry(title, newcontent)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": newcontent
        })
    else:
        return render(request, "encyclopedia/newpage.html")
    
def editpage(request, title):
    
    if request.method == "POST":
        newtitle = request.POST.get("title")
        newcontent = request.POST.get("newcontent")
        util.save_entry(newtitle, newcontent)
        if util.get_entry(newtitle):
            util.delete_entry(title)
        return render(request, "encyclopedia/entry.html", {
            "title": newtitle,
            "content": newcontent
        })
    else:
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "content": util.get_entry(title)
        })