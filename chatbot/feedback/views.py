from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .models import Feedback
from django_filters.views import FilterView
from django.views.generic import DetailView

# Create your views here.
@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class FeedbackDetailView(DetailView):
    model = Feedback
    template_name = 'feedback/feedback_detail.html'
    context_object_name = 'feedback'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feedback = self.get_object()
        context['feedback'] = feedback
        return context

@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class FeedbackFilterView(FilterView):
    model = Feedback
    template_name = 'feedback/feedback_list.html'
    context_object_name = 'feedbacks'

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedbacks'] = Feedback.objects.all()
        return context
    
def contact_view(request):
    return render(request, "feedback/contact.html")

class FeedbackView(generic.CreateView):
    model = Feedback
    fields = ['email', 'subject', 'description']
    template_name = 'feedback/contact.html'
    success_url = reverse_lazy('home:home')
    
    # success_url = '/edit_profile'
    
    def form_valid(self, form):
        print("form_valid", form)
        if form.is_valid():
            self.object = form.save()
            messages.success(self.request, f'Feedback sent successfully')
            return super().form_valid(form)
        else:
            # Log form errors
            print(form.errors)
            return self.form_invalid(form)
        
def delete_feedback(request, pk):
    feedback = Feedback.objects.get(pk=pk)
    feedback.delete()
    return render(request, "feedback/feedback_list.html")
