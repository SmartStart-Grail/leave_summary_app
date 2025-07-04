# Generated by Django 5.0.4 on 2024-05-22 10:57

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='country_metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(default=datetime.datetime(2024, 5, 22, 16, 27, 3, 773445))),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Country MetaData',
                'verbose_name_plural': 'Country MetaData',
            },
        ),
        migrations.CreateModel(
            name='department_metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(default=datetime.datetime(2024, 5, 22, 16, 27, 3, 773445))),
                ('dept_code', models.IntegerField()),
                ('dept_name', models.CharField(max_length=100)),
                ('dept_description', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Department Metadata',
                'verbose_name_plural': 'Department Metadata',
            },
        ),
        migrations.CreateModel(
            name='employee_metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(default=datetime.datetime(2024, 5, 22, 16, 27, 3, 773445))),
                ('employee_id', models.IntegerField()),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('work_email', models.EmailField(max_length=254)),
                ('job_title', models.CharField(max_length=100)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave_app.department_metadata')),
                ('work_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave_app.country_metadata')),
            ],
            options={
                'verbose_name': 'Employee Metadata',
                'verbose_name_plural': 'Employee Metadata',
            },
        ),
        migrations.CreateModel(
            name='holiday_metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(default=datetime.datetime(2024, 5, 22, 16, 27, 3, 773445))),
                ('holiday_name', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('year', models.IntegerField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave_app.country_metadata')),
            ],
            options={
                'verbose_name': 'Holiday Metadata',
                'verbose_name_plural': 'Holiday Metadata',
            },
        ),
        migrations.CreateModel(
            name='indirectsupervisor_metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(default=datetime.datetime(2024, 5, 22, 16, 27, 3, 773445))),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave_app.employee_metadata')),
            ],
            options={
                'verbose_name': 'Indirectsupervisor Metadata',
                'verbose_name_plural': 'Indirectsupervisor Metadata',
            },
        ),
        migrations.CreateModel(
            name='leave_metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(default=datetime.datetime(2024, 5, 22, 16, 27, 3, 773445))),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('hours', models.IntegerField()),
                ('request_status', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave_app.employee_metadata')),
            ],
            options={
                'verbose_name': 'Leave Metadata',
                'verbose_name_plural': 'Leave Metadata',
            },
        ),
        migrations.CreateModel(
            name='supervisor_metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(default=datetime.datetime(2024, 5, 22, 16, 27, 3, 773445))),
                ('employee_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_data', to='leave_app.employee_metadata')),
                ('indirect_supervisor_metadata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave_app.indirectsupervisor_metadata')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor', to='leave_app.employee_metadata')),
            ],
            options={
                'verbose_name': 'Supervisor Metadata',
                'verbose_name_plural': 'Supervisor Metadata',
            },
        ),
    ]
