from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',) +UserCreationForm.Meta.fields
    
    def clean_username(self):
        if CustomUser.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError("Użytkownik o tej nazwie już istnieje.")
        return self.cleaned_data['username']

    def clean_email(self):
        if CustomUser.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("Podany adres email już istnieje.")
        return self.cleaned_data['email']
            
class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields

    
