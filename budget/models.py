from django.db import models


# Create your models here.
class LineItem(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=20)
    date_stamp = models.DateField()
    amount = models.FloatField()
