# Generated by Django 2.2.5 on 2020-09-06 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_ative',
            field=models.BooleanField(default=False, verbose_name='邮箱验证状态'),
        ),
    ]
