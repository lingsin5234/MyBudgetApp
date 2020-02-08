from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import LineItem, ExpCategory, CreditCard, ExpenseLineItem
from .models import RevCategory, BankAccount, RevenueLineItem
from .forms import UploadLineItemForm, UploadExpCatForm, UploadCreditCardForm, UploadExpenseForm
from .forms import UploadRevCatForm, UploadBankAccountForm, UploadRevenueForm
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.forms.models import model_to_dict


# line item test view
def show_data(request):
    items = LineItem.objects.all()

    context = {
        'line_items': items
    }
    return render(request, 'pages/display.html', context)


# d3.js test view
def show_d3(request):

    # serialize all LineItem objects and convert to json format
    items = ExpenseLineItem.objects.all()
    category = ExpCategory.objects.all()
    revenue = RevenueLineItem.objects.all()
    output = []
    cats = []
    revs = []
    for item in items:
        add = model_to_dict(item)
        output.append(add)
        # output[i] = add
        # i += 1
    for cat in category:
        add = model_to_dict(cat)
        cats.append(add)
    # output = json.dumps(items[:])
    data = [30, 65, 300]
    json_data = [
        {
            "x_axis": 30,
            "y_axis": 30,
            "radius": 20,
            "color": "purple",
        },
        {
            "x_axis": 65,
            "y_axis": 65,
            "radius": 20,
            "color": "orange",
        },
        {
            "x_axis": 200,
            "y_axis": 200,
            "radius": 20,
            "color": "green",
        }
    ]
    expenses = [
        {
            "id": 1,
            "name": "McDonalds",
            "category": "Food",
            "amount": 12.40
        },
        {
            "id": 2,
            "name": "Gateway Entertainment",
            "category": "Activities",
            "amount": 11.00
        }
    ]
    bank_info = [
        {
            "id": 1,
            "name": "Cash",
            "colour": "#660066",
            "amount": "50.00"
        },
        {
            "id": 2,
            "name": "RBC",
            "colour": "#005daa",
            "amount": "25000.00"
        },
        {
            "id": 3,
            "name": "Tangerine",
            "colour": "#f28500",
            "amount": "1700.00"
        }
    ]
    for rev in revenue:
        add = model_to_dict(rev)
        revs.append(add)

    context = {
        'expense': json.dumps(output, cls=DjangoJSONEncoder),
        'category': json.dumps(cats),
        'revenue': json.dumps(revs, cls=DjangoJSONEncoder),
        'bank_info': json.dumps(bank_info),
        'data': data,
        'json_data': json.dumps(json_data),
        # 'line_items': output,
        'type': output[0]
        # 'expenses': json.dumps(expenses)
    }
    return render(request, 'pages/d3_test.html', context)


def upload_data(request, upload_type):
    # default upload_name
    upload_name = 'Expense Item'

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        if upload_type == 'expense':
            form = UploadExpenseForm(request.POST)
        elif upload_type == 'credit_card':
            upload_name = 'Credit Card'
            form = UploadCreditCardForm(request.POST)
        elif upload_type == 'exp_category':
            upload_name = 'Expense Category'
            form = UploadExpCatForm(request.POST)
        elif upload_type == 'revenue':
            upload_name = 'Revenue Item'
            form = UploadRevenueForm(request.POST)
        elif upload_type == 'rev_category':
            upload_name = 'Revenue Category'
            form = UploadRevCatForm(request.POST)
        elif upload_type == 'bank_account':
            upload_name = 'Bank Account'
            form = UploadBankAccountForm(request.POST)
        else:
            upload_name = 'Line Item'
            form = UploadLineItemForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/upload_done/' + upload_type + '/')

    # if a GET (or any other method) we'll create a blank form
    else:
        if upload_type == 'expense':
            form = UploadExpenseForm()
        elif upload_type == 'credit_card':
            upload_name = 'Credit Card'
            form = UploadCreditCardForm()
        elif upload_type == 'exp_category':
            upload_name = 'Expense Category'
            form = UploadExpCatForm()
        elif upload_type == 'revenue':
            upload_name = 'Revenue Item'
            form = UploadRevenueForm()
        elif upload_type == 'rev_category':
            upload_name = 'Revenue Category'
            form = UploadRevCatForm()
        elif upload_type == 'bank_account':
            upload_name = 'Bank Account'
            form = UploadBankAccountForm()
        else:
            upload_name = 'Line Item'
            form = UploadLineItemForm

    context = {
        'form': form,
        'upload_type': upload_type,
        'upload_name': upload_name
    }

    return render(request, 'pages/upload.html', context)


def upload_done(request, upload_type):
    if upload_type == 'expense':
        upload_name = 'Expense Item'
        item = ExpenseLineItem.objects.latest('pk')
    elif upload_type == 'credit_card':
        upload_name = 'Credit Card'
        item = CreditCard.objects.latest('pk')
    elif upload_type == 'exp_category':
        upload_name = 'Category'
        item = ExpCategory.objects.latest('pk')
    elif upload_type == 'revenue':
        upload_name = 'Revenue Item'
        item = RevenueLineItem.objects.latest('pk')
    elif upload_type == 'rev_category':
        upload_name = 'Revenue Category'
        item = RevCategory.objects.latest('pk')
    elif upload_type == 'bank_account':
        upload_name = 'Bank Account'
        item = BankAccount.objects.latest('pk')
    else:
        upload_name = 'Line Item'
        item = LineItem.objects.latest('pk')

    context = {
        'upload_type': upload_type,
        'upload_name': upload_name,
        'item': item
    }
    return render(request, 'pages/upload_done.html', context)
