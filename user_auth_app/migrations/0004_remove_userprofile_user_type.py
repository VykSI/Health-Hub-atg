# Generated by Django 5.0 on 2023-12-08 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth_app', '0003_delete_mm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_type',
        ),
    ]
