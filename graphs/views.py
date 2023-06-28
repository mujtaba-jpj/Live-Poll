from django.shortcuts import render
from .models import PollChoices, Poll
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    poll = Poll.objects.get(name='Web dev')
    
    return render(request, 'graphs/index.html',{'poll':poll})
