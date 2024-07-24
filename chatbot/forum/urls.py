from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.AllForumsView, name="home"),
    path("<int:id>", views.SingleForumView, name="forum"),
]
