# Generated by Django 3.0.2 on 2020-02-08 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0017_creditcard_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]
