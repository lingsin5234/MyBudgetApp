from django import forms
from .models import LineItem, ExpCategory, CreditCard, ExpenseLineItem, CreditCardPayment
from .models import RevCategory, BankAccount, RevenueLineItem, BankLineItem


class UploadLineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = ['name', 'category', 'date_stamp', 'amount']


class UploadExpCatForm(forms.ModelForm):
    class Meta:
        model = ExpCategory
        fields = ['name', 'colour']


class UploadCreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['name']


class UploadExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpenseLineItem
        fields = ['name', 'category', 'pay_type', 'card_name', 'date_stamp', 'amount']


class UploadRevCatForm(forms.ModelForm):
    class Meta:
        model = RevCategory
        fields = ['name', 'colour']


class UploadBankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['nickname', 'bank_name', 'account_type', 'balance']


class UploadRevenueForm(forms.ModelForm):
    class Meta:
        model = RevenueLineItem
        fields = ['name', 'category', 'cash_debit', 'bank_account', 'date_stamp', 'amount']


class UploadBankLineItemForm(forms.ModelForm):
    class Meta:
        model = BankLineItem
        fields = ['amount', 'from_transaction', 'to_transaction', 'date_stamp']


class UploadCreditCardPaymentForm(forms.ModelForm):
    class Meta:
        model = CreditCardPayment
        fields = ['amount', 'from_bank', 'to_credit_card', 'date_stamp']
