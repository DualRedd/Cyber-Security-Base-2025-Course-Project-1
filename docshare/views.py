from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm



@login_required
def index(request):
    return render(request, 'docshare/pages/index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'docshare/registration/register.html', {'form': form})


