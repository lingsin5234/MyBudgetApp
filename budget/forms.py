from django import forms
from .models import LineItem


class UploadDataForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = ['name', 'category', 'date_stamp', 'amount']
