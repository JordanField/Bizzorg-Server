# Generated by Django 2.1.5 on 2019-02-09 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('deadline_date', models.DateField(blank=True, null=True)),
                ('priority', models.CharField(choices=[('low', 'Low priority'), ('reg', 'Regular'), ('sig', 'Significant'), ('urg', 'Urgent'), ('sev', 'Severe')], default='reg', max_length=3)),
                ('employees', models.ManyToManyField(blank=True, related_name='delegated_tasks', to='groups.EmployeeProfile')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_do_list_items', to='groups.EmployeeGroup')),
            ],
        ),
    ]
