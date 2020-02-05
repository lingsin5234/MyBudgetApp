from django.contrib import admin
from .models import LineItem, ExpCategory, CreditCard, ExpenseLineItem
from .models import RevCategory, BankAccount, RevenueLineItem

# Register your models here.
admin.site.register(LineItem)
admin.site.register(ExpCategory)
admin.site.register(CreditCard)
admin.site.register(ExpenseLineItem)
admin.site.register(RevCategory)
admin.site.register(BankAccount)
admin.site.register(RevenueLineItem)
