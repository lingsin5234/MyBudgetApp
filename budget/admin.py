from django.contrib import admin
from .models import LineItem, Category, CreditCard, ExpenseLineItem

# Register your models here.
admin.site.register(LineItem)
admin.site.register(Category)
admin.site.register(CreditCard)
admin.site.register(ExpenseLineItem)
