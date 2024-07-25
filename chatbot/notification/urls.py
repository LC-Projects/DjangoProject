from django.urls import path, include
from . import views

urlpatterns = [
    path("list/", views.FeedbackFilterView.as_view(), name="notification_list"),
    path("create/", views.NotificationView.as_view(), name="create"),
]
