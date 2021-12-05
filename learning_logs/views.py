from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import TopicForm, EntryForm
from .models import Topic, Entry
# Create your views here.

def check_topic_owner(request, topic):
    return True if request.user == topic.owner else False
  
def index(request):
    """Home page for Learning logs app."""
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    """ Display all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """ Display one topic and all his entries."""
    
    topic = get_object_or_404(Topic, pk=topic_id)
    
    if not check_topic_owner(request, topic):
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = { 'topic': topic,
                'entries': entries,
            }
    return render(request, 'learning_logs/topic.html', context)
    
@login_required
def new_topic(request):
    """ Adding new topic from user """

    if request.method != 'POST':
        form = TopicForm(request.user)
    else:
        form = TopicForm(request.user, data=request.POST)
        print(request.POST)
        if form.is_valid():

            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """ Adding new entry to specific topic"""
    
    topic = get_object_or_404(Topic, pk=topic_id)
    
    if not check_topic_owner(request, topic):
        raise Http404

    if request.method != 'POST':
        form = EntryForm(topic)
    else:
        form = EntryForm(topic, data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id)
        
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit entry of topic"""
    
    entry = get_object_or_404(Entry, pk=entry_id)
    topic = entry.topic

    if not check_topic_owner(request, topic):
        raise Http404

    if request.method != 'POST':
        form = EntryForm(topic, instance=entry)
    else:
        form = EntryForm(topic, instance=entry, data=request.POST)
        form.save()
        return redirect('learning_logs/topic', topic.id)

    context = {'topic': topic, 'entry': entry, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
    

@login_required
def delete_entry(request, entry_id):
    """Delete entry of topic"""

    entry = get_object_or_404(Entry, pk=entry_id)
    entry.delete()

    return render(request, 'learning_logs/topic', topic.id)
 
    