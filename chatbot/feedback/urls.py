from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.FeedbackView.as_view(), name='contact'),
    path("list/", views.FeedbackFilterView.as_view(), name="feedback_list"),
    path("detail/<int:pk>/", views.FeedbackDetailView.as_view(), name="feedback_detail"),
    path("delete/<int:pk>/", views.delete_feedback, name="feedback_delete"),
]
