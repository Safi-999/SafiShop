from django import forms
from django.forms import CharField
from django.forms import widgets
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': ''
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': ''
    }))
    class Meta :
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
         super(RegistrationForm, self).__init__(*args, **kwargs)
    #    self.fields['first_name'].widget.attrs['placeholder'] = 'Entrez votre Prénom'
    #    self.fields['last_name'].widget.attrs['placeholder'] = 'Entrez votre Nom'
    #    self.fields['phone_number'].widget.attrs['placeholder'] = 'Entrez votre Numéro de téléphone'
    #    self.fields['email'].widget.attrs['placeholder'] = 'Entrez votre Adresse Email'
    #    for field in self.fields:
    #        self.fields[field].widget.attrs['class'] = 'form-control'


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Mots de passe no identiques !'
            )



