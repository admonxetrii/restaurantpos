# Generated by Django 3.2.5 on 2021-08-26 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='service_amnt',
            field=models.FloatField(blank=True, null=True),
        ),
    ]