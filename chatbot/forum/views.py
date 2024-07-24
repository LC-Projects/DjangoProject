from django.shortcuts import render

# Create your views here.

def AllForumsView(request):
    template_name = 'forum/home.html'
    
    
    return render(request, template_name)