from django.urls import path, include
from . import views

urlpatterns = [
    path(
        "",
            include(
                [
                    path("list/", views.ChatFilterView.as_view(), name="chat_list"),
                    path("detail/<int:pk>/", views.ChatDetailView.as_view(), name="chat_detail"),
                    path("public/detail/<int:pk>/", views.PublicChatDetailView.as_view(), name="public_chat_detail"),
                    path("delete/", views.chat_delete, name="chat_delete"),
                    path('add_message/', views.add_message, name='add_message'),
                    path('create_chat/', views.create_chat, name='create_chat'),
                    path('change-private/', views.change_private, name='change_private'),
                    path('add_comment/', views.add_comment, name='add_comment'),
                ]
            ),
    ),
]
