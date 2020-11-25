from django.forms import ModelForm, TextInput
from .models import User_reg

class LoginForm(ModelForm):
    class Meta:
        model = User_reg
        fields = ['username', 'password']

        widgets = {
            'password': TextInput(attrs = {
                'type': 'password',
                'placeholder': 'Пароль',
                'required': ''
            }),
            'username': TextInput(attrs = {
                'type': 'text',
                'placeholder': 'Логин',
                'required': ''
                })
        }

class RegForm(ModelForm):
    class Meta:
        model = User_reg
        fields = ['username', 'password', 'password_c']

        widgets = {
            'password': TextInput(attrs = {
                'type': 'password',
                'placeholder': 'Пароль',
                'required': ''
            }),
            'username': TextInput(attrs = {
                'type': 'text',
                'placeholder': 'Логин',
                'required': ''
                }),
            'password_c': TextInput(attrs = {
                'type': 'password',
                'placeholder': 'Подтверждение пароля',
                'required': ''
                })
        }
