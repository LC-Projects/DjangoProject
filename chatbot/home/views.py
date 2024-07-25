from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, "home/home.html")

def about_view(request):
    return render(request, "home/about.html")

def licensing_view(request):
    return render(request, "home/licensing.html")

def privacy_view(request):
    return render(request, "home/privacy.html")