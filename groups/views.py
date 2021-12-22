from django.contrib.auth.decorators import login_required
from django.urls.base import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from learning_logs.models import Topic
from groups.forms import MyGroupForm, NewMemberForm
from .models import MyGroup
from users.models import CustomUser
# Create your views here.




def check_group_admin(group, request):
    return True if group.admin == request.user else False

class GroupsView(LoginRequiredMixin, generic.ListView):
    template_name= 'groups/groups.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return MyGroup.objects.filter(user=self.request.user)


class NewGroupView(LoginRequiredMixin, generic.FormView):
    template_name = 'groups/new_group.html'
    form_class = MyGroupForm
    success_url = '/groups/'

    def get_form_kwargs(self):
        kwargs = super(NewGroupView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        new_group = form.save(commit=False)
        new_group.admin = self.request.user
        new_group.save()
        new_group.user_set.add(self.request.user)
        return super().form_valid(form)


class DeleteGroupView(LoginRequiredMixin, generic.DeleteView):
    model = MyGroup
    success_url = reverse_lazy("groups:groups")
    context_object_name = 'group'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if check_group_admin(self.object, request):
            return super(DeleteGroupView, self).delete(
                request, *args, **kwargs)
        else:
            raise Http404

@login_required
def new_group(request):
    """ Create new_group """
    
    if request.method != "POST":
        form = MyGroupForm(request.user)
    else:
        form = MyGroupForm(request.user,data=request.POST)
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.admin = request.user
            new_group.save()
            new_group.user_set.add(request.user)

            return redirect('groups:groups')
    
    context = {'form': form}
    return render(request, 'groups/new_group.html', context)

@login_required
def group(request, group_id):
    """ Display one group and all his topics and users"""

    group = get_object_or_404(MyGroup, pk=group_id)
    topics = Topic.objects.filter(group=group,access="grp")
    if not request.user.groups.filter(id=group.id):
        raise Http404

    if not check_group_admin(group, request):
        context = {'group': group,'topics': topics, 'admin': False}
        return render(request,'groups/group.html', context)    

    context = {'group': group,'topics': topics, 'admin': True}

    return render(request,'groups/group.html', context)



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
            user =  CustomUser.objects.filter(username=form.cleaned_data['username'])
            group.user_set.add(user.get().id)
            return redirect('groups:group', group.id)

    context = {'group': group, 'form': form}
    return render(request, 'groups/add_to_group.html', context)


@login_required
def delete_from_group(request, group_id):
    """ Panel with users available to delete"""

    group = get_object_or_404(MyGroup, pk=group_id)

    if not check_group_admin(group, request) or \
        len(group.user_set.all()) < 2:
        raise Http404
    
    return render(request, 'groups/delete_from_group.html', {'group':group})


@login_required
def delete_user(request, group_id, user_id):
    """ Panel confirming the removal of the member """

    group = get_object_or_404(MyGroup,pk=group_id)
    user = get_object_or_404(CustomUser,pk=user_id)
    
    if not check_group_admin(group,request) or \
        user == group.admin:
        raise Http404
    
    if request.method == 'POST':
        group.user_set.remove(user)
        return redirect('groups:group', group_id)
  
    context = {'user': user, 'group': group}

    return render(request,'groups/member_confirm_delete.html', context)
