from django import forms
from .models import Topic, Entry
 

class TopicForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.owner = user;
    class Meta:
        model = Topic
        fields = ['text', 'access']
        labels = {'text':'', 'access':'Dostęp'}

    def clean_text(self):
        text = self.cleaned_data['text']
        if Topic.objects.filter(text__iexact=text, owner=self.owner).exists():
            raise forms.ValidationError("Temat o tej nazwie już istnieje", code="topic_exists")
        return text

class TopicAccessForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ['access']
        labels = {'access': ''}

class EntryForm(forms.ModelForm):

    def __init__(self, topic, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.topic = topic


    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}
    
    # def clean_text(self):
    #     text = self.cleaned_data['text']
    #     if Entry.objects.filter(text__iexact=text, topic=self.topic).exists():
    #         raise forms.ValidationError("Taki wpis juz istnieje")
    #     return text

        