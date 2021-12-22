from django.contrib.auth import login
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from groups.models import MyGroup
from .forms import GroupTopicForm, TopicAccessForm, TopicForm, EntryForm
from .models import Topic, Entry
# Create your views here.

def check_topic_owner(request, topic):
    return True if request.user == topic.owner else False
  
def index(request):
    """Home page for Learning logs app."""
    return render(request,'notes/index.html')

@login_required
def topics(request):
    """ Display all topics."""
    topics_public = Topic.objects.filter(access="pub").exclude(owner=request.user).order_by('date_added')
    topics_private = Topic.objects.filter(owner=request.user).exclude(access='grp').order_by('date_added')
    context = {'topics_public': topics_public,
               'topics_private': topics_private}
    

    return render(request, 'notes/topics.html', context)

@login_required
def topic(request, topic_id):
    """ Display one topic and all his entries."""
    
    changed = False
    topic = get_object_or_404(Topic, pk=topic_id)
    
    if not check_topic_owner(request, topic) and \
       topic.access == "priv":
        raise Http404
    

    entries = topic.entry_set.order_by('-date_added')

    if not check_topic_owner(request, topic):
        context = { 'topic': topic,
                'entries': entries,
                
                }
        return render(request, 'notes/topic.html', context)
    
    if request.method != 'POST':
        form = TopicAccessForm(instance=topic)
    else:
        form = TopicAccessForm(instance=topic,data=request.POST)
        changed = True
        if form.is_valid():
            form.save()
        
    context = { 'topic': topic,
                'entries': entries,
                'form': form,
                'changed': changed
            }
    return render(request, 'notes/topic.html', context)
    
@login_required
def new_topic(request):
    """ Adding new topic from user """

    if request.method != 'POST':
        form = TopicForm(request.user)
    else:
        form = TopicForm(request.user, data=request.POST)
        if form.is_valid():

            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('notes:topics')

    context = {'form': form}
    return render(request, 'notes/new_topic.html', context)

@login_required
def delete_topic(request, topic_id):
    """ Deleting topic """

    topic = get_object_or_404(Topic, pk=topic_id);

    if not check_topic_owner(request,topic):
        raise Http404

    if request.method == 'POST':
        if topic.group == -1:
            topic.delete()
            return redirect('notes:topics')
        else:
            group = topic.group.id
            topic.delete()
            return redirect('groups:group', group)
    
    return render(request,'notes/delete_topic.html', {'topic': topic})


@login_required
def new_entry(request, topic_id):
    """ Adding new entry to specific topic"""
    
    topic = get_object_or_404(Topic, pk=topic_id)
    
    if not check_topic_owner(request, topic) and \
        topic.access == "priv":
        raise Http404

    if request.method != 'POST':
        form = EntryForm(topic)
    else:
        form = EntryForm(topic,data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.creator = request.user
            new_entry.topic = topic
            new_entry.save()
            return redirect('notes:topic', topic_id)
        
    context = {'topic': topic, 'form': form}
    return render(request, 'notes/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit entry of topic"""
    
    entry = get_object_or_404(Entry, pk=entry_id)
    topic = entry.topic

    if not check_topic_owner(request, topic) and \
        topic.access == "priv" or request.user != entry.creator:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(topic, instance=entry)
    else:
        form = EntryForm(topic, instance=entry, data=request.POST)
        if form.is_valid():
        
            form.save()
            return redirect('notes:topic', topic.id)

    context = {'topic': topic, 'entry': entry, 'form': form}
    return render(request, 'notes/edit_entry.html', context)
    

@login_required
def delete_entry(request, entry_id):
    """Delete entry of topic"""

    entry= get_object_or_404(Entry, pk=entry_id);
    topic = entry.topic
    if request.user != entry.creator:
        raise Http404
        
    if request.method == 'POST':
        entry.delete()
        return redirect('notes:topic', topic.id)    
    
    return render(request,'notes/delete_entry.html', {'topic': topic})



@login_required
def group_new_topic(request, group_id):
    """ Add topic to group """
    group = get_object_or_404(MyGroup, pk=group_id)


    if not request.user.groups.filter(id=group.id):
        raise Http404

    if request.method != 'POST':
        form = GroupTopicForm(group)
    else:
        form = GroupTopicForm(group, data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.group = group
            new_topic.access = 'grp'
            new_topic.owner = request.user
            new_topic.save()
        
            return redirect('groups:group', group.id)
    
    context = {'form': form, 'group': group}

    return render(request,'notes/group_new_topic.html', context)