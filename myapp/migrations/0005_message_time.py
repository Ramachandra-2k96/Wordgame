# Generated by Django 3.2.6 on 2023-12-27 07:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_message_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]