# Generated by Django 2.1.5 on 2019-02-09 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import groups.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_position', models.CharField(blank=True, max_length=100)),
                ('profile_picture', models.ImageField(blank=True, upload_to=groups.models.user_directory_path)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_privileges', models.BooleanField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='groups.EmployeeProfile')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.EmployeeGroup')),
            ],
        ),
        migrations.AddField(
            model_name='employeegroup',
            name='members',
            field=models.ManyToManyField(related_name='employee_groups', through='groups.GroupMembership', to='groups.EmployeeProfile'),
        ),
        migrations.AddField(
            model_name='employeegroup',
            name='parent_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='groups.EmployeeGroup'),
        ),
    ]
