# Generated by Django 5.0 on 2024-01-13 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0017_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='post-media/'),
        ),
    ]
