# Generated by Django 3.0.2 on 2020-02-05 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0008_auto_20200205_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=15)),
                ('bank_name', models.CharField(blank=True, default=None, max_length=15, null=True)),
                ('account_type', models.CharField(max_length=15)),
                ('balance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RevCategory',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('colour', models.CharField(default=None, max_length=7, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RevenueLineItem',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('cash_debit', models.CharField(max_length=10)),
                ('date_stamp', models.DateField()),
                ('amount', models.FloatField()),
                ('bank_account', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='budget.BankAccount')),
                ('category', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='budget.RevCategory')),
            ],
        ),
    ]
