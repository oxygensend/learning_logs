from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from learning_logs.models import Topic



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


