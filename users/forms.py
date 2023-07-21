
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'input', 'placeholder': 'Confirm Password'})

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'input', 'placeholder': 'Password'})


'''
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    pass

'''