from django.db import models


# Create your models here.
class TestData(models.Model):
    name = models.CharField(max_length=120)
    amount = models.FloatField()
    category = models.CharField(max_length=120)
