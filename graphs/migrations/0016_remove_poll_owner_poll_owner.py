# Generated by Django 4.1.3 on 2023-07-19 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('graphs', '0015_poll_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='owner',
        ),
        migrations.AddField(
            model_name='poll',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]