# Generated by Django 5.0 on 2023-12-24 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0007_alter_review_created_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='notification_status',
        ),
        migrations.RemoveField(
            model_name='like',
            name='notification_status',
        ),
    ]
