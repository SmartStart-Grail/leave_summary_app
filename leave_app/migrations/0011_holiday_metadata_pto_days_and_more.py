# Generated by Django 5.0.4 on 2024-05-29 12:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0010_alter_country_metadata_modified_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday_metadata',
            name='pto_days',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='country_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 29, 17, 30, 33, 586294)),
        ),
        migrations.AlterField(
            model_name='department_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 29, 17, 30, 33, 586294)),
        ),
        migrations.AlterField(
            model_name='employee_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 29, 17, 30, 33, 586294)),
        ),
        migrations.AlterField(
            model_name='holiday_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 29, 17, 30, 33, 586294)),
        ),
        migrations.AlterField(
            model_name='indirectsupervisor_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 29, 17, 30, 33, 586294)),
        ),
        migrations.AlterField(
            model_name='leave_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 29, 17, 30, 33, 586294)),
        ),
        migrations.AlterField(
            model_name='supervisor_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 29, 17, 30, 33, 586294)),
        ),
        migrations.AlterField(
            model_name='uploadleave_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 29, 17, 30, 33, 586294)),
        ),
    ]
