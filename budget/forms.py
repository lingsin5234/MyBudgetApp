from django import forms


class UploadData(forms.Form):
    line_item = forms.CharField(label='Line Item', max_length=30)
    category = forms.CharField(label='Category', max_length=20)
    date_stamp = forms.DateField(label='Date')
    amount = forms.FloatField(label='Amount')
