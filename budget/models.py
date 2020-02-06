from django.db import models


# Expense Category
class ExpCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    colour = models.CharField(max_length=7, null=True, default=None)

    def __str__(self):
        return self.name


# Revenue Category
class RevCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    colour = models.CharField(max_length=7, null=True, default=None)

    def __str__(self):
        return self.name


# Line Item
class LineItem(models.Model):
    name = models.CharField(max_length=30)
    category = models.OneToOneField(ExpCategory, on_delete=models.SET_DEFAULT, default='Uncategorized')
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


# Bank Account / Cash
class BankAccount(models.Model):
    id = models.IntegerField(primary_key=True)
    nickname = models.CharField(max_length=15, unique=True)
    bank_name = models.CharField(max_length=15, null=True, blank=True, default=None)
    account_type = models.CharField(max_length=15)
    balance = models.FloatField()

    def __str__(self):
        return self.nickname

    def show_all(self):
        return ["Nickname: " + self.nickname,
                "Bank Name: " + str(self.bank_name),
                "Account Type: " + self.account_type,
                "Balance: $" + str(self.balance)]


# Expenses Line Item
class ExpenseLineItem(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    category = models.ForeignKey(ExpCategory, on_delete=models.SET_DEFAULT, default='Uncategorized')
    pay_type = models.CharField(max_length=10)
    card_name = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    date_stamp = models.DateField()
    amount = models.FloatField()

    def __str__(self):
        return self.name


# Revenue Line Item
class RevenueLineItem(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    category = models.ForeignKey(RevCategory, on_delete=models.SET_DEFAULT, default='Uncategorized')
    cash_debit = models.CharField(max_length=10)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.SET_DEFAULT, default='Missing Bank')
    date_stamp = models.DateField()
    amount = models.FloatField()

    def __str__(self):
        return self.name
