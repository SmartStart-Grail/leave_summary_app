# Generated by Django 5.0.4 on 2024-05-27 05:48

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0004_alter_country_metadata_modified_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_metadata',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='country_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 27, 11, 18, 16, 738284)),
        ),
        migrations.AlterField(
            model_name='department_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 27, 11, 18, 16, 738284)),
        ),
        migrations.AlterField(
            model_name='employee_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 27, 11, 18, 16, 738284)),
        ),
        migrations.AlterField(
            model_name='holiday_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 27, 11, 18, 16, 738284)),
        ),
        migrations.AlterField(
            model_name='indirectsupervisor_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 27, 11, 18, 16, 738284)),
        ),
        migrations.AlterField(
            model_name='leave_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 27, 11, 18, 16, 738284)),
        ),
        migrations.AlterField(
            model_name='supervisor_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 27, 11, 18, 16, 738284)),
        ),
    ]
