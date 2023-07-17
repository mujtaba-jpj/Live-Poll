from django.shortcuts import render, redirect
from .models import PollChoices, Poll
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages


def index(request):
    return render(request, 'graphs/index.html')


@login_required
def poll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    print(poll)
    return render(request, 'graphs/poll.html', {'poll': poll})


def LoginUser(request):
    if request.user.is_authenticated:
        messages.error(request, 'Already logged in')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print('USername .... ', username)
        print('password .... ', password)
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Account does not exist with that email')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password is incorrect')

    return render(request, 'graphs/register_login_form.html')

@login_required(login_url='login-user')
def LogoutUser(request):
    logout(request)
    messages.success(request, 'User was succesfully logged out')

    return redirect('home')


def createPoll(request):
    
    return render(request,'graphs/poll_form.html')