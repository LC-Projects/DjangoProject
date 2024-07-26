from django import forms
from crispy_forms.helper import FormHelper
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['login'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Enter Username', 'id': 'username'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Enter Password', 'id': 'password'})
        self.fields['remember'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})


class UserRegistrationForm(SignupForm):

    # Redéfinir l'ordre des champs dans le formulaire
    field_order = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control mb-1', 'placeholder': 'Entrez un nom d\'utilisateur', 'id': 'username1'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control textInput', 'placeholder': 'Entrez un mot de passe', 'id': 'password1'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control textInput', 'placeholder': 'Confirmez votre mot de passe', 'id': 'password2'})
        self.fields['password2'].label = "Confirmez votre mot de passe"
        
        
        

class EditUserForm(UserChangeForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                'placeholder': 'Enter Email', 
                'id': 'email'
            }))    
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Enter Username',
                'id': 'username'
            }))
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                'placeholder': 'Enter First Name', 
                'id': 'first_name'
            }))
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                'placeholder': 'Enter Last Name', 
                'id': 'last_name'
            }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        exclude = [ 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined']