from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("random", views.random_entry, name="random"),
    path("wiki/<str:title>", views.show_entry, name="show_entry"),
    path("create", views.create_entry, name="create"),
    path("wiki/<str:title>/edit", views.edit_entry, name="edit")

]
