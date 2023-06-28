from django.contrib import admin
from .models import PollChoices, Poll
# Register your models here.

admin.site.register(PollChoices)
admin.site.register(Poll)
