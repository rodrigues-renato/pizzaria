from django import forms
from django.contrib.auth import forms as form_user
from .models import CustomUser
from django.core.exceptions import ValidationError


class UserChangeForm(form_user.UserChangeForm):
    class Meta(form_user.UserChangeForm.Meta):
        models = CustomUser


class UserCreationForm(form_user.UserCreationForm):
    class Meta(form_user.UserCreationForm.Meta):
        models = CustomUser


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )

    last_name = forms.CharField(
        required=True,
        min_length=3,
    )

    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'cpf',
            'rua',
            'bairro',
            'numero',
            'telefone',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            self.add_error(
                'email', ValidationError('E-mail already exists', code='invalid')
            )

        return email
    
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user