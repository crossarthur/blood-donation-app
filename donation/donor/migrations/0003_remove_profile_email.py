# Generated by Django 4.2.5 on 2023-09-16 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0002_remove_profile_first_name_remove_profile_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]
