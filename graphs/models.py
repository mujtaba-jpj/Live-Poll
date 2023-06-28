from django.db import models
import random
from django.contrib.auth.models import User
from django.db.models import Sum
# Create your models hre.


def generate_random_code():
    code = random.randint(10000000, 99999999)
    return str(code)


class Poll(models.Model):
    uuid = generate_random_code()
    id = models.CharField(
        primary_key=True, default='poll-'+str(uuid), editable=False,max_length=50)
    name = models.CharField(max_length=100, null=False, blank=False)
    total_votes = models.IntegerField(default=0)
    # options = models.ManyToManyField('PollChoices')

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.total_votes = self.options.aggregate(Sum('choice_votes'))['choice_votes__sum'] or 0
        super().save(*args, **kwargs)
        
        
class PollChoices(models.Model):
    poll_rs = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options',null=True)
    voters = models.ManyToManyField(User, blank=True)
    choice_name = models.CharField(max_length=70, null=False, blank=False)
    choice_votes = models.SmallIntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.choice_name
