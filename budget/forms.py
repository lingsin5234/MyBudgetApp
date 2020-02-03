from django import forms
from .models import LineItem, Category, CreditCard, ExpenseLineItem


class UploadLineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = ['name', 'category', 'date_stamp', 'amount']


class UploadCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class UploadCreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['name']


class UploadExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpenseLineItem
        fields = ['name', 'category', 'pay_type', 'card_name', 'date_stamp', 'amount']
