# Generated by Django 5.0 on 2023-12-16 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='notification_status',
            field=models.CharField(choices=[('See', 'See'), ('Saw', 'Saw')], default='See', max_length=3),
        ),
        migrations.AddField(
            model_name='like',
            name='notification_status',
            field=models.CharField(choices=[('See', 'See'), ('Saw', 'Saw')], default='See', max_length=3),
        ),
    ]
