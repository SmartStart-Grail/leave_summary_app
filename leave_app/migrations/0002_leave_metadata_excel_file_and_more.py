# Generated by Django 5.0.4 on 2024-05-23 11:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave_metadata',
            name='excel_file',
            field=models.FileField(blank=True, null=True, upload_to='static/excel_folder/'),
        ),
        migrations.AlterField(
            model_name='country_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 23, 16, 52, 8, 934207)),
        ),
        migrations.AlterField(
            model_name='department_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 23, 16, 52, 8, 934207)),
        ),
        migrations.AlterField(
            model_name='employee_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 23, 16, 52, 8, 934207)),
        ),
        migrations.AlterField(
            model_name='holiday_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 23, 16, 52, 8, 934207)),
        ),
        migrations.AlterField(
            model_name='indirectsupervisor_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 23, 16, 52, 8, 934207)),
        ),
        migrations.AlterField(
            model_name='leave_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 23, 16, 52, 8, 934207)),
        ),
        migrations.AlterField(
            model_name='supervisor_metadata',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 23, 16, 52, 8, 934207)),
        ),
    ]
