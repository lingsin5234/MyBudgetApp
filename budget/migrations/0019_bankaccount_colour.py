# Generated by Django 3.0.2 on 2020-02-08 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0018_auto_20200208_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='colour',
            field=models.CharField(default='#FFFFFF', max_length=7),
        ),
    ]
