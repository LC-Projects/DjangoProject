from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from pyexpat.errors import messages
from django.urls import reverse_lazy
from django.views import generic
from .models import Notification
from django_filters.views import FilterView

@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class NotificationView(generic.CreateView):
    model = Notification
    fields = ['user', 'slug', 'chatId']
    template_name = 'home/home.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            messages.success(self.request, f'Notification sent successfully')
            return super().form_valid(form)
        else:
            # Log form errors
            print(form.errors)
            return self.form_invalid(form)

@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class FeedbackFilterView(FilterView):
    model = Notification
    template_name = 'notification/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notifications'] = Notification.objects.all()
        return context