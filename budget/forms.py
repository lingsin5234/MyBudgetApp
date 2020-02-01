from django import forms
from .models import LineItem, Category


class UploadLineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = ['name', 'category', 'date_stamp', 'amount']


class UploadCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
