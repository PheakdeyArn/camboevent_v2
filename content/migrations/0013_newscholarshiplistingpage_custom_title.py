# Generated by Django 3.2.13 on 2022-06-22 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_newscholarshiplistingpage_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='newscholarshiplistingpage',
            name='custom_title',
            field=models.CharField(default='', help_text='Overwrites the default title', max_length=100),
            preserve_default=False,
        ),
    ]
