from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import MyGroup

class MyGroupForm(forms.ModelForm):

    class Meta:
        model = MyGroup
        fields = ['name']
        labels = {'name': 'Podaj nazwe'}

class NewMemberForm(forms.Form):
    username = forms.CharField(label='Podaj nazwe użytkownika', max_length=100)
    def clean_text(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user.exists():
            return user.id
        else:
            raise ValidationError("Taki użytkownik nie istnieje", code="user_does_not_exist")
