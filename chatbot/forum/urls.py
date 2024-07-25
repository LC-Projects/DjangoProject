from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.AllForumsView, name="home"),
    path("<slug:slug>/", views.ForumByCategoryView, name="home_slug"),
]
