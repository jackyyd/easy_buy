# Generated by Django 2.2.5 on 2020-09-10 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_auto_20200910_1055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sku',
            old_name='scales',
            new_name='sales',
        ),
    ]