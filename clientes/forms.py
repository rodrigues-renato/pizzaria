from django import forms
from django.contrib.auth import forms as _forms
from .models import CustomUser, EnderecoUser
from django.core.exceptions import ValidationError


class UserChangeForm(_forms.UserChangeForm):
    class Meta(_forms.UserChangeForm.Meta):
        models = CustomUser


class UserCreationForm(_forms.UserCreationForm):
    class Meta(_forms.UserCreationForm.Meta):
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
            'telefone',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            self.add_error(
                'email', ValidationError('E-mail já existe', code='invalid')
            )

        return email
    
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AddressForm(forms.ModelForm):
    class Meta:
        model = EnderecoUser
        fields = ('rua', 'bairro', 'numero')
        