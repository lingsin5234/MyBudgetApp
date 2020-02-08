from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import LineItem, ExpCategory, CreditCard, ExpenseLineItem
from .models import RevCategory, BankAccount, RevenueLineItem
from .forms import UploadLineItemForm, UploadExpCatForm, UploadCreditCardForm, UploadExpenseForm
from .forms import UploadRevCatForm, UploadBankAccountForm, UploadRevenueForm, UploadBankLineItemForm
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


# get bank line item form data from the revenue line item input
def get_rev_data(post_data):
    # get some objects to input correct reference
    withdrawal = RevCategory.objects.get(name="Withdrawal")
    deposit = RevCategory.objects.get(name="Deposit")
    cash = BankAccount.objects.get(nickname="Cash")

    # if Withdrawal:
    if post_data['category'] == str(withdrawal.id):
        rev_data = {
            'amount': post_data['amount'],
            'from_transaction': post_data['bank_account'],
            'to_transaction': str(cash.id),
            'date_stamp': post_data['date_stamp']
        }
    # if Deposit:
    elif post_data['category'] == str(deposit.id):
        rev_data = {
            'amount': post_data['amount'],
            'from_transaction': str(cash.id),
            'to_transaction': post_data['bank_account'],
            'date_stamp': post_data['date_stamp']
        }
    else:
        rev_data = {
            'amount': post_data['amount'],
            'from_transaction': '',
            'to_transaction': post_data['bank_account'],
            'date_stamp': post_data['date_stamp']
        }
    return rev_data


# get bank line item form data from the expense line item input
def get_exp_data(post_data):
    exp_data = {
        'amount': post_data['amount'],
        'from_transaction': '',
        'to_transaction': post_data['credit_card'],
        'date_stamp': post_data['date_stamp']
    }
    return exp_data


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

            # check if it's expense or revenue line item
            if upload_type == 'expense':
                # expense then get expenses then submit bank form
                exp_data = get_exp_data(request.POST)
                form2 = UploadBankLineItemForm(exp_data)

                if form2.is_valid():
                    form2.save()
                else:
                    HttpResponse('<h1>Bank Line Item Form error</h1>')
            elif upload_type == 'revenue':
                # revenue then get rev data then submit bank form
                rev_data = get_rev_data(request.POST)
                # return HttpResponse('<p>' + str(rev_data) + '</p><p>' + request.POST['category'] + '</p>')
                form2 = UploadBankLineItemForm(rev_data)

                if form2.is_valid():
                    form2.save()
                else:
                    HttpResponse('<h1>Bank Line Item Form error</h1>')
            # still need to save the first form
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
