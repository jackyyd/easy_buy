# Generated by Django 2.2.5 on 2020-09-09 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='img',
            new_name='image',
        ),
    ]
