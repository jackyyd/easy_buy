# Generated by Django 2.2.5 on 2020-09-12 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0010_auto_20200910_1221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sku',
            old_name='default_image',
            new_name='default_image_url',
        ),
    ]
