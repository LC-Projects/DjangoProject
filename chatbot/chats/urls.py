from django.urls import path, include
from . import views

urlpatterns = [
    path(
        "",
            include(
                [
                    path("list/<int:category>/", views.chat_list, name="chat_list"),
                    path("detail/<int:pk>/", views.ChatDetailView.as_view(), name="chat_detail"),
                    path("delete/", views.chat_delete, name="chat_delete"),
                    path('add_message/', views.add_message, name='add_message'),
                ]
            ),
    ),
]
