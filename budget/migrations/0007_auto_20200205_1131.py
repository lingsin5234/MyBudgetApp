# Generated by Django 3.0.2 on 2020-02-05 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0006_auto_20200205_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='expenselineitem',
            name='card_name',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget.CreditCard'),
        ),
    ]