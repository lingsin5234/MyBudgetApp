from django.db import models


# Line Item Category
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# Line Item
class LineItem(models.Model):
    name = models.CharField(max_length=30)
    category = models.OneToOneField(Category, on_delete=models.SET_DEFAULT, default='Uncategorized')
    date_stamp = models.DateField()
    amount = models.FloatField()

    def __str__(self):
        return self.name


# Credit Card
class CreditCard(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


# Expenses Line Item
class ExpenseLineItem(models.Model):
    name = models.CharField(max_length=30)
    category = models.OneToOneField(Category, on_delete=models.SET_DEFAULT, default='Uncategorized')
    pay_type = models.CharField(max_length=10)
    card_name = models.OneToOneField(CreditCard, on_delete=models.SET_NULL, null=True, default=None)
    date_stamp = models.DateField()
    amount = models.FloatField()

    def __str__(self):
        return self.name
