from django.urls import path

from . import views

app_name = 'quotes_app'

urlpatterns = [
    path("", views.main, name="main"),
    path("author_detail/<int:author_id>/", views.author_detail, name="author_detail"),
    path("page/<int:page>", views.main, name="main_paginate"),
    path("tag/", views.tag, name="tag"),
    path("quote/", views.quote, name="quote"),
    path("author/", views.author, name="author")
]
