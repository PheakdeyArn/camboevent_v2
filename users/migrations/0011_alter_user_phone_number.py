# Generated by Django 3.2.13 on 2022-06-03 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=24, null=True, unique=True, verbose_name='Phone Number'),
        ),
    ]
