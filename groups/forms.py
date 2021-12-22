from django import forms
from users.models import CustomUser
from django.core.exceptions import ValidationError
from .models import MyGroup

class MyGroupForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(MyGroupForm, self).__init__(*args, **kwargs)
        self.user = user;
    class Meta:
        model = MyGroup
        fields = ['name']
        labels = {'name': 'Podaj nazwe'}

    def clean_name(self):
        user = self.user.groups.filter(name=self.cleaned_data['name'])

        if user.exists():
            raise ValidationError("Grupa o takiej nazwie już istnieje", code="group_same_name")
      
        else:
            return self.cleaned_data['name']
class NewMemberForm(forms.Form):
    
    
    def __init__(self, group, *args, **kwargs):
        super(NewMemberForm, self).__init__(*args, **kwargs)
        self.group = group;
    
    username = forms.CharField(label='Podaj nazwe użytkownika', max_length=100)
    def clean_username(self):
        username = self.cleaned_data['username']
        user = CustomUser.objects.filter(username=username)
        user1 = user.filter(groups__name=self.group.name)
        if not user.exists():
            raise ValidationError("Taki użytkownik nie istnieje", code="user_does_not_exist")
        elif  user1.exists():
            raise ValidationError("Ten użytkownik został już dodany do grupy", code="user_exists_in_group")
        else: 
            return username
            

