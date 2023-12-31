# Generated by Django 4.2.1 on 2023-06-28 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainPoll', '0007_alter_poll_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='options',
        ),
        migrations.AddField(
            model_name='pollchoices',
            name='poll_rs',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='mainPoll.poll'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='id',
            field=models.CharField(default='poll-45658832', editable=False,
                                   max_length=50, primary_key=True, serialize=False),
        ),
    ]
