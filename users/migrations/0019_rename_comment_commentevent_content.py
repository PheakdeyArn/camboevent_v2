# Generated by Django 3.2.13 on 2022-06-23 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20220623_1848'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentevent',
            old_name='comment',
            new_name='content',
        ),
    ]
