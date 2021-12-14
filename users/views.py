from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from learning_logs.models import Topic

from users.forms import MyGroupForm, NewMemberForm
from .models import MyGroup
# Create your views here.


def check_group_admin(group, request):
    return True if group.admin == request.user else False

def register(request):
    """ New user registration """

    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            new_login = form.save()
            login(request, new_login)
            return redirect('learning_logs:index')
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)


class GroupsView(generic.ListView):
    template_name= 'registration/groups.html'
    context_object_name = 'groups'

    def get_queryset(self):

        return MyGroup.objects.all()

@login_required
def groups(request):

    return render(request,'registration/groups.html', {'groups':MyGroup.objects.all()})

@login_required
def new_group(request):
    """ Create new_group """
    
    if request.method != "POST":
        form = MyGroupForm()
    else:
        form = MyGroupForm(data=request.POST)
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.admin = request.user
            new_group.save()
            new_group.user_set.add(request.user)

            return redirect('users:groups')
    
    context = {'form': form}
    return render(request, 'registration/new_group.html', context)

@login_required
def group(request, group_id):
    """ Display one group and all his topics and users"""

    group = get_object_or_404(MyGroup, pk=group_id)
    topics = Topic.objects.filter(group=group)
    if not check_group_admin(group, request):
        context = {'group': group, 'admin': False}
        return render(request,'registration/group.html', context)    

    context = {'group': group,'topics': topics, 'admin': True}

    return render(request,'registration/group.html', context)


@login_required
def delete_group(request, group_id):
    """Delete group"""

    group= get_object_or_404(MyGroup, pk=group_id);

    if not check_group_admin(group, request):
        raise Http404
        
    if request.method == 'POST':
        group.delete()
        return redirect('users:groups')    
    
    return render(request,'registration/delete_group.html', {'group': group})

@login_required
def add_to_group(request, group_id):
    """ Add new member to group """

    group = get_object_or_404(MyGroup, pk=group_id)

    if not check_group_admin(group, request):
        raise Http404

    if request.method != 'POST':
        form = NewMemberForm(group)
    else:
        form = NewMemberForm(group, data=request.POST)
        if form.is_valid():
            user =  User.objects.filter(username=form.cleaned_data['username']).exclude(groups__name=group.name)
            group.user_set.add(user.get().id)
            return redirect('users:group', group.id)

    context = {'group': group, 'form': form}
    return render(request, 'registration/add_to_group.html', context)


