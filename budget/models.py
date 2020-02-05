from django.db import models


# Category
class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    colour = models.CharField(max_length=7, null=True, default=None)

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
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15, null=True, blank=True, default=None)

    def __str__(self):
        return self.name


# Expenses Line Item
class ExpenseLineItem(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='Uncategorized')
    pay_type = models.CharField(max_length=10)
    card_name = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    date_stamp = models.DateField()
    amount = models.FloatField()

    def __str__(self):
        return self.name
