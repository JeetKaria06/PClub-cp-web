# Generated by Django 3.1 on 2020-08-22 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_remove_leaderboard_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='tags',
            field=models.TextField(default='', max_length=100000),
        ),
    ]
