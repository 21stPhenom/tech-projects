# Generated by Django 5.0.1 on 2024-02-22 09:58

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='solution',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]