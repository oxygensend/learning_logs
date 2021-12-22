from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import FilteredSelectMultiple    
from notes.models import Topic
from .models import MyGroup
from django.contrib.auth.admin import GroupAdmin
from django import forms

from users.models import CustomUser
#
# Register your models here.



class TopicInline(admin.TabularInline):

    model = Topic
    
   


class GroupAdminForm(forms.ModelForm):

    class Meta:
        model = MyGroup
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
         queryset=CustomUser.objects.all(), 
         required=False,
         # Use the pretty 'filter_horizontal widget'.
         widget=FilteredSelectMultiple('users', False)
    )

    admin = forms.ModelChoiceField(queryset=CustomUser.objects.all(),
         required=True)

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all() 
            
    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])
        self.instance.user_set.add(self.cleaned_data['admin'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance

class MyGroupAdmin(admin.ModelAdmin):

    form = GroupAdminForm
    def user_count(self, obj):
        return obj.user_set.count()

    list_display = GroupAdmin.list_display + ('user_count','admin') 
    search_fields = ['name']
#    list_display = ['text','date_added','access','owner',(user_count,)]
    fieldsets = [ (None, {'fields': ['name','admin','users']}),]
    
    sortable_by = ('user_count',)
    inlines = [TopicInline]


admin.site.register(MyGroup, MyGroupAdmin)