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
