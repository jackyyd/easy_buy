# Generated by Django 2.2.5 on 2020-09-07 02:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('areas', '0001_initial'),
        ('users', '0003_auto_20200906_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=True)),
                ('title', models.CharField(max_length=20, verbose_name='地址名称')),
                ('receiver', models.CharField(max_length=20, verbose_name='收货人')),
                ('place', models.CharField(max_length=50, verbose_name='详细地址')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号')),
                ('tel', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='固定电话')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_address', to='areas.Area', verbose_name='市')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='district_address', to='areas.Area', verbose_name='区')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='province_address', to='areas.Area', verbose_name='省')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'db_table': 'tb_address',
                'ordering': ['-update_time'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='default_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='users.Address', verbose_name='默认收货地址'),
        ),
    ]
