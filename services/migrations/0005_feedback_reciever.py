# Generated by Django 5.0.3 on 2024-03-10 08:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_feedback_read_feedback_sender'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='reciever',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='reciever', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
