from django.contrib import admin
from .models import Topic, Entry
# Register your models here.


class EntryInline(admin.TabularInline):

    model = Entry
 
class TopicAdmin(admin.ModelAdmin):

    search_fields = ['text']
    list_filter = ['date_added']
    list_display = ['text','date_added','access','owner']
   
    
    inlines = [EntryInline]

admin.site.register(Topic, TopicAdmin)



