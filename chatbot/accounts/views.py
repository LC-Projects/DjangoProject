from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserRegistrationForm, UserLoginForm, EditUserForm
from .models import Profile, User

from chats.models import Chat


def register_view(request):
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
    fields = ['bio', 'avatar', 'birthdate', 'emotion', 'location', 'language']
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['languages'] = [
            {'code': 'us', 'name': 'English'},
            {'code': 'es', 'name': 'Spanish'},
            {'code': 'fr', 'name': 'French'},
            {'code': 'de', 'name': 'German'},
        ]
        return context


def profile_view(request, username):
    template_name = 'accounts/profile.html'
    context = {}

    user = User.objects.get(username=username)

    context['user_data'] = user

    datas_chats = []
    chats = Chat.objects.filter(user=user, is_private=False)
    for chat in chats:
        datas_chats.append({
            'id': chat.id,
            'name': chat.name,
            'created_at': chat.created_at,
        })

    context['datas_chats'] = datas_chats

    return render(request, template_name, context)

def edit_mood(request):
    if request.method == "POST":
        user = request.user
        profile = Profile.objects.get(user=user)
        profile.emotion = request.POST['emotion']
        profile.save()
        messages.success(request, f'Mood updated to {profile.emotion}')
        return redirect('home:home')
    else:
        return redirect('home:home')

class ChangePasswordView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy("user_profile")

    def post(self, request, *args, **kwargs):
        old_password: str = request.POST.get("old_password")
        new_password1: str = request.POST.get('new_password1')
        new_password2: str = request.POST.get('new_password2')

        user = request.user

        if not user.check_password(old_password):
            messages.warning(request, "old password doesn't match.")
            return redirect("auth:password")

        if len(new_password1) < 10:
            messages.warning(request, "password length should not be less than 10.")
            return redirect("auth:password")

        if old_password == new_password1:
            messages.warning(request, "your new password cannot be the same as your old password.")
            return redirect("auth:password")

        if new_password1 != new_password2:
            messages.warning(request, "new_password1 and new_password2 do not match.")
            return redirect("auth:password")

        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "password change successfull. your new password would take effect on next login.")
        logout(request)

        return redirect("auth:login")