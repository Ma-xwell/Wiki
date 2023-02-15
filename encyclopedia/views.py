from django.shortcuts import render, redirect, reverse
from . import util
import random
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html", {
            "error": 404
        })
    # Finding an index of the title in order to prompt it on the page case insensitively
    index = [x.lower() for x in util.list_entries()].index(title.lower())
    return render(request, "encyclopedia/entry.html", {
        "title": util.list_entries()[index],
        "content": markdown2.markdown(util.get_entry(title))
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
            return redirect("encyclopedia:entry", title=util.list_entries()[index])
        # If the user has not provided the full title, then look if the query is a substring
        # in any of existing pages' titles 
        else:
            result_list = []
            for i in range(len(util.list_entries())):
                if q.lower() in util.list_entries()[i].lower():
                    result_list.append(util.list_entries()[i])    
            return render(request, "encyclopedia/search.html", {
                    "query": q,
                    "result_list": result_list
            })
            
def newpage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        # Additional checks in case user bypassed frontend requirements
        # or if article with given title already exists
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
        return redirect("encyclopedia:entry", title=str(title))
    else:
        return render(request, "encyclopedia/newpage.html")
    
def editpage(request, title):
    
    if request.method == "POST":
        if request.POST.get("button") == "delete":
            util.delete_entry(title)
            return redirect("encyclopedia:index")
        newtitle = request.POST.get("newtitle")
        newcontent = request.POST.get("newcontent")
        if title == newtitle:
            util.delete_entry(title)
            util.save_entry(newtitle, newcontent)
        else:
            if newtitle in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "error": "Such article already exists"
                })
            util.delete_entry(title)
            util.save_entry(newtitle, newcontent)
        
        return redirect("encyclopedia:entry", title=str(newtitle))
    else:
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "content": util.get_entry(title)
        })

def randompage(request):
    list_of_titles = util.list_entries()
    # Getting random index of list of titles
    index = random.randint(0, len(list_of_titles) - 1)
    title = list_of_titles[index]
    return redirect("encyclopedia:entry", title=str(title))