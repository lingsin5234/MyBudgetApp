from django.db import models


# CHOICES
CASH_DEBIT = [('cash', 'cash'),
              ('debit', 'debit')]
PAY_TYPE = [('cash', 'cash'),
            ('debit', 'debit'),
            ('credit', 'credit')]


# Expense Category
class ExpCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    colour = models.CharField(max_length=7, null=True, default=None)

    def __str__(self):
        return self.name

    def show_all(self):
        return ["Expense Category:", self.name,
                "Colour:", self.colour]


# Revenue Category
class RevCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    colour = models.CharField(max_length=7, null=True, default=None)

    def __str__(self):
        return self.name

    def show_all(self):
        return ["Revenue Category:", self.name,
                "Colour:", self.colour]


# Line Item
class LineItem(models.Model):
    name = models.CharField(max_length=30)
    category = models.OneToOneField(ExpCategory, on_delete=models.SET_DEFAULT, default='Uncategorized')
    date_stamp = models.DateField()
    amount = models.FloatField()

    def __str__(self):
        return self.name

    def show_all(self):
        return ["Line Item:", self.name,
                "Category:", self.category,
                "Date:", str(self.date_stamp),
                "Amount:", "$" + str(self.amount)]


# Credit Card
class CreditCard(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15, null=True, blank=True, default=None)
    colour = models.CharField(max_length=7, null=True, default=None)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def show_all(self):
        return ["Credit Card:", self.name,
                "Colour:", self.colour]


# Bank Account / Cash
class BankAccount(models.Model):
    id = models.IntegerField(primary_key=True)
    nickname = models.CharField(max_length=15, unique=True)
    bank_name = models.CharField(max_length=15, null=True, blank=True, default=None)
    account_type = models.CharField(max_length=15)
    balance = models.FloatField()
    colour = models.CharField(max_length=7, default='#FFFFFF')

    def __str__(self):
        return self.nickname

    def show_all(self):
        return ["Nickname:", self.nickname,
                "Bank Name:", str(self.bank_name),
                "Account Type:", self.account_type,
                "Balance:", "$" + str(self.balance),
                "Colour:", self.colour]


# Expenses Line Item
class ExpenseLineItem(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    category = models.ForeignKey(ExpCategory, on_delete=models.SET_DEFAULT, default='Uncategorized')
    pay_type = models.CharField(max_length=6, choices=PAY_TYPE)
    card_name = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    date_stamp = models.DateField()
    amount = models.FloatField()

    def __str__(self):
        return self.name

    def show_all(self):
        return ["Expense:", self.name,
                "Category:", self.category,
                "Payment:", self.pay_type,
                "Card Name:", self.card_name,
                "Date:", str(self.date_stamp),
                "Amount:", "$" + str(self.amount)]


# Revenue Line Item
class RevenueLineItem(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    category = models.ForeignKey(RevCategory, on_delete=models.SET_DEFAULT, default='Uncategorized')
    cash_debit = models.CharField(max_length=5, choices=CASH_DEBIT)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.SET_DEFAULT, default='Missing Bank')
    date_stamp = models.DateField()
    amount = models.FloatField()

    def __str__(self):
        return self.name

    def show_all(self):
        return ["Revenue:", self.name,
                "Category:", self.category,
                "Cash/Debit:", self.cash_debit,
                "Bank Account:", self.bank_account,
                "Date:", str(self.date_stamp),
                "Amount:", "$" + str(self.amount)]


# Bank Account Transactional Items
class BankLineItem(models.Model):
    id = models.IntegerField(primary_key=True)
    amount = models.FloatField()
    from_transaction = models.ForeignKey(BankAccount, null=True, blank=True,
                                         on_delete=models.SET_NULL, related_name='_unused_1')
    to_transaction = models.ForeignKey(BankAccount, null=True, blank=True,
                                       on_delete=models.SET_NULL, related_name='_unused_2')
    date_stamp = models.DateField()

    def __str__(self):
        return "From " + str(self.from_transaction) + " To " + str(self.to_transaction) + ": $" + str(self.amount) + \
               " on " + str(self.date_stamp) + "."


# Credit Card Payment
class CreditCardPayment(models.Model):
    id = models.IntegerField(primary_key=True)
    amount = models.FloatField()
    from_bank = models.ForeignKey(BankAccount, on_delete=models.SET_DEFAULT, default='_defunct_acct')
    to_credit_card = models.ForeignKey(CreditCard, on_delete=models.SET_DEFAULT, default='_defunct_cc')
    date_stamp = models.DateField()

    def __str__(self):
        return "From " + str(self.from_bank) + " To " + str(self.to_credit_card) + ": $" + str(self.amount) + \
               " on " + str(self.date_stamp) + "."

    def show_all(self):
        return ["From:", self.from_bank,
                "To:", self.to_credit_card,
                "Date:", str(self.date_stamp),
                "Amount:", "$" + str(self.amount)]
