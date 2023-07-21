from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import PollChoices, Poll
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'mainPoll/index.html')


@login_required
def poll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    return render(request, 'mainPoll/poll.html', {'poll': poll})


def LoginUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Already logged in')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in')
                return redirect('home')
            else:
                messages.warning(request, 'Username OR Password is incorrect')
        except:
            messages.warning(
                request, 'Account does not exist with that username')

    return render(request, 'mainPoll/register_login_form.html')


@login_required(login_url='login-user')
def LogoutUser(request):
    logout(request)
    messages.success(request, 'User was succesfully logged out')

    return redirect('home')


@login_required(login_url='login-user')
def createPoll(request):

    if request.method == 'POST':
        pollName = request.POST['pollName']
        pollOpts = request.POST.getlist('pollOptVal')

        if len(pollOpts) == len(set(pollOpts)):
            pollCreation = Poll.objects.create(
                name=pollName,
                owner=request.user,
            )
            for opt in pollOpts:
                PollChoices.objects.create(
                    poll_rs=pollCreation,
                    choice_name=opt,
                )
            return redirect('/poll/'+pollCreation.id)
        else:
            messages.warning(
                request, 'You cannot have options with the same name')

    return render(request, 'mainPoll/poll_form.html')


@login_required(login_url='login-user')
def myPolls(request):

    userPolls = Poll.objects.filter(owner=request.user)
    if userPolls.exists():
        context = {'userPolls': userPolls}
        return render(request, 'mainPoll/my_polls.html', context)
    else:
        messages.warning(request, 'No Polls found created by this user')
        return redirect('home')


@csrf_exempt
def deletePoll(request):
    pollId = request.POST['pollId']
    fetchPoll = Poll.objects.get(id=pollId)
    fetchPoll.delete()

    messages.success(request, 'Poll deleted succesfully')
    return JsonResponse({'status': 1})
