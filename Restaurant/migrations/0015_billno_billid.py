# Generated by Django 3.0.4 on 2020-12-13 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0014_order_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='billno',
            name='billid',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
