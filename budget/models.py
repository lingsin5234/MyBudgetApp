from django.db import models


# CHOICES
CASH_DEBIT = [('cash', 'cash'),
              ('debit', 'debit')]
PAY_TYPE = [('cash', 'cash'),
            ('debit', 'debit'),
            ('credit', 'credit')]


# Expense Category
class ExpCategory(models.Model):
    name = models.CharField(max_length=20)
    colour = models.CharField(max_length=7, null=True, default=None)

    def __str__(self):
        return self.name

    def show_all(self):
        return ["Expense Category:", self.name,
                "Colour:", self.colour]


# Revenue Category
class RevCategory(models.Model):
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
    category = models.OneToOneField(ExpCategory, on_delete=models.SET_DEFAULT, default=0)
    date_stamp = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=9)

    def __str__(self):
        return self.name

    def show_all(self):
        return ["Line Item:", self.name,
                "Category:", self.category,
                "Date:", str(self.date_stamp),
                "Amount:", "$" + str(self.amount)]


# Credit Card
class CreditCard(models.Model):
    nickname = models.CharField(max_length=15, null=True, blank=True, default=None)
    colour = models.CharField(max_length=7, null=True, default=None)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=9)

    def __str__(self):
        return self.nickname

    def show_all(self):
        return ["Credit Card:", self.nickname,
                "Colour:", self.colour]


# Bank Account / Cash
class BankAccount(models.Model):
    nickname = models.CharField(max_length=15, unique=True)
    bank_name = models.CharField(max_length=15, null=True, blank=True, default=None)
    account_type = models.CharField(max_length=15)
    balance = models.DecimalField(decimal_places=2, max_digits=9)
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
    name = models.CharField(max_length=30)
    category = models.ForeignKey(ExpCategory, on_delete=models.SET_DEFAULT, default=0)
    pay_type = models.CharField(max_length=6, choices=PAY_TYPE)
    card_name = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    date_stamp = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=9)

    def __str__(self):
        return self.name

    def show_all(self):
        return ["Expense:", self.name,
                "Category:", self.category,
                "Payment:", self.pay_type,
                "Card Name:", self.card_name,
                "Bank Account:", self.bank_account,
                "Date:", str(self.date_stamp),
                "Amount:", "$" + str(self.amount)]


# Revenue Line Item
class RevenueLineItem(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(RevCategory, on_delete=models.SET_DEFAULT, default=0)
    cash_debit = models.CharField(max_length=5, choices=CASH_DEBIT)
    bank_account = models.ForeignKey(BankAccount, null=True, on_delete=models.SET_NULL)
    date_stamp = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=9)

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
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    from_transaction = models.ForeignKey(BankAccount, null=True, blank=True,
                                         on_delete=models.SET_NULL, related_name='_unused_1')
    to_transaction = models.ForeignKey(BankAccount, null=True, blank=True,
                                       on_delete=models.SET_NULL, related_name='_unused_2')
    date_stamp = models.DateField()

    def __str__(self):
        return "From " + str(self.from_transaction) + " To " + str(self.to_transaction) + ": $" + str(self.amount) + \
               " on " + str(self.date_stamp) + "."


# Credit Card Account Transactional Items
class CreditCardLineItem(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    to_credit_card = models.ForeignKey(CreditCard, null=True, on_delete=models.SET_NULL)
    date_stamp = models.DateField()

    def __str__(self):
        return "Expense Item credited to " + str(self.to_credit_card) + " for: $" + str(self.amount) + \
               " on " + str(self.date_stamp) + "."


# Credit Card Payment
class CreditCardPayment(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    from_bank = models.ForeignKey(BankAccount, null=True, on_delete=models.SET_NULL)
    to_credit_card = models.ForeignKey(CreditCard, null=True, on_delete=models.SET_NULL)
    date_stamp = models.DateField()

    def __str__(self):
        return "From " + str(self.from_bank) + " To " + str(self.to_credit_card) + ": $" + str(self.amount) + \
               " on " + str(self.date_stamp) + "."

    def show_all(self):
        return ["From:", self.from_bank,
                "To:", self.to_credit_card,
                "Date:", str(self.date_stamp),
                "Amount:", "$" + str(self.amount)]
