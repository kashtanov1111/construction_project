from allauth.account.forms import SignupForm, LoginForm

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username')

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']:
            self.fields[key].label = False
        
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()      
        return user

class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = False
        self.fields['password'].label = False
