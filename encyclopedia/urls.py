from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("wiki/edit/<str:title>", views.editpage, name="editpage"),
    path("wiki", views.randompage, name="randompage")
]
