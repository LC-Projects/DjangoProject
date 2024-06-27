from django.urls import path, include
from . import views

urlpatterns = [
    path(
        "",
            include(
                [
                    path("list/<int:category>/", views.chat_list, name="chat_list"),
                    path("detail/<int:chat>/", views.chat_detail, name="chat_detail"),
                ]
            ),
    ),
]
