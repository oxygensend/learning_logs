from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

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

