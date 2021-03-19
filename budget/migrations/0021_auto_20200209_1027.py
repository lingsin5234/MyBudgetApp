# Generated by Django 3.0.2 on 2020-02-09 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0020_auto_20200209_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcardpayment',
            name='from_bank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget.BankAccount'),
        ),
        migrations.AlterField(
            model_name='creditcardpayment',
            name='to_credit_card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget.CreditCard'),
        ),
        migrations.AlterField(
            model_name='revenuelineitem',
            name='bank_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget.BankAccount'),
        ),
    ]