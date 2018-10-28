# Generated by Django 2.1.2 on 2018-10-28 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='locationID',
            new_name='location',
        ),
        migrations.AddField(
            model_name='location',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='long',
            field=models.FloatField(null=True),
        ),
    ]
