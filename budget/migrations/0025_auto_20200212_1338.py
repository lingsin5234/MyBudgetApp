# Generated by Django 3.0.2 on 2020-02-12 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0024_auto_20200212_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]
