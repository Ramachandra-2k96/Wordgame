# Generated by Django 3.2.6 on 2023-12-27 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_rename_user_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='CMessage',
            new_name='computer_response',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='Message',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='username',
            new_name='user',
        ),
    ]