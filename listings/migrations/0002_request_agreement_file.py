# Generated by Django 4.2.4 on 2023-09-11 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='agreement_file',
            field=models.FileField(blank=True, null=True, upload_to='deal/agreements'),
        ),
    ]
