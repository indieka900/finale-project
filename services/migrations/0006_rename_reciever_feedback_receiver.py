# Generated by Django 5.0.3 on 2024-04-06 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_feedback_reciever'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='reciever',
            new_name='receiver',
        ),
    ]
