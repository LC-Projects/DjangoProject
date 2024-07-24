from django.shortcuts import render

# Create your views here.
def AllNotificationView(request):
    template_name = 'notification/notification.html'
    return render(request, template_name)