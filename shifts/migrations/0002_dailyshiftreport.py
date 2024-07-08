# Generated by Django 5.0.6 on 2024-07-07 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyShiftReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('report_file', models.FileField(upload_to='daily_shift_reports/')),
            ],
        ),
    ]
