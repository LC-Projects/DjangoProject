from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserRegistrationForm, UserLoginForm, EditUserForm
from .models import Profile
from django.shortcuts import get_object_or_404



def register_view(request):
    print("register_view", request.POST)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            
            Profile.objects.create(user=user)
            
            messages.success(request, f'Account created for {form.cleaned_data["username"]}')

    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


class login_view(generic.FormView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home:home')
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
    
    def form_invalid(self, form):
        error_messages = ''
        for field, errors in form.errors.items():
            for error in errors:
                error_messages += f"{field}: {error}\n"
        messages.error(self.request, error_messages)
        return super().form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('home:home')



class UserEditView(generic.UpdateView):
    form_class = EditUserForm
    template_name = 'accounts/edit_user.html'
    success_url = reverse_lazy('auth:edit_user')
    
    def get_object(self):
        return self.request.user
    
    
class UserProfileEditView(generic.UpdateView):
    model = Profile
    fields = ['bio', 'avatar', 'birthdate']
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('auth:edit_profile')
    
    # success_url = '/edit_profile'
    
    def form_valid(self, form):
        print("form_valid", form)
        if form.is_valid():
            self.object = form.save()
            messages.success(self.request, f'Profile updated for {self.request.user}')
            return super().form_valid(form)
        else:
            # Log form errors
            print(form.errors)
            return self.form_invalid(form)
    
    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile