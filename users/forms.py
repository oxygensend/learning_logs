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
    
    
    def __init__(self, group, *args, **kwargs):
        super(NewMemberForm, self).__init__(*args, **kwargs)
        self.group = group;
    
    username = forms.CharField(label='Podaj nazwe użytkownika', max_length=100)
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        user1 = user.exclude(groups__name=self.group.name)
        if not user1.exists():
            raise ValidationError("Ten użytkownik został już dodany do grupy", code="user_exists_in_group")
        elif user.exists():
            return username
        else:
            raise ValidationError("Taki użytkownik nie istnieje", code="user_does_not_exist")
