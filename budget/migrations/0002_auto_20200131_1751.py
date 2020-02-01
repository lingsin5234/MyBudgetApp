# Generated by Django 3.0.2 on 2020-02-01 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='category',
            field=models.OneToOneField(default='Uncategorized', on_delete=django.db.models.deletion.SET_DEFAULT, to='budget.Category'),
        ),
    ]
