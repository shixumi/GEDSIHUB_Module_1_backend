# Generated by Django 5.0.7 on 2024-08-09 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
