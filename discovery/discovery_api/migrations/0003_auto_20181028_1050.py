# Generated by Django 2.1.2 on 2018-10-28 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery_api', '0002_auto_20181028_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='long',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
