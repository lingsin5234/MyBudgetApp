from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from .models import LineItem, ExpCategory, CreditCard, ExpenseLineItem
from .models import BankLineItem, CreditCardLineItem
from .models import RevCategory, BankAccount, RevenueLineItem, CreditCardPayment
from .forms import UploadLineItemForm, UploadExpCatForm, UploadCreditCardForm, UploadExpenseForm
from .forms import UploadRevCatForm, UploadBankAccountForm, UploadRevenueForm, UploadBankLineItemForm
from .forms import UploadCreditCardPaymentForm, UploadCreditCardLineItemForm
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.forms.models import model_to_dict
from .functions import get_exp_data, get_rev_data, update_bank_rev, credit_card_payment, update_bank_exp
import logging

# create logger instance
# logger = logging.getLogger(__name__)


# line item test view
def show_data(request):
    items = LineItem.objects.all()

    context = {
        'line_items': items
    }
    return render(request, 'pages/display.html', context)


# d3.js test view
def show_d3(request):

    # convert all objects from dict_to_model
    items = ExpenseLineItem.objects.all()
    category = ExpCategory.objects.all()
    revenue = RevenueLineItem.objects.all()
    bank = BankAccount.objects.all()
    cc = CreditCard.objects.all()
    bank_line = BankLineItem.objects.all().order_by('-date_stamp')
    cc_line = CreditCardLineItem.objects.all().order_by('-date_stamp')
    cc_pay = CreditCardPayment.objects.all().order_by('-date_stamp')
    output = []
    cats = []
    revs = []
    banks = []
    ccs = []
    bank_lines = []
    cc_lines = []
    cc_pays = []
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
    for b in bank:
        add = model_to_dict(b)
        banks.append(add)
    for c in cc:
        add = model_to_dict(c)
        ccs.append(add)
    for bl in bank_line:
        add = model_to_dict(bl)
        bank_lines.append(add)
    for cl in cc_line:
        add = model_to_dict(cl)
        cc_lines.append(add)
    for cp in cc_pay:
        add = model_to_dict(cp)
        cc_pays.append(add)

    context = {
        'expense': json.dumps(output, cls=DjangoJSONEncoder),
        'category': json.dumps(cats),
        'revenue': json.dumps(revs, cls=DjangoJSONEncoder),
        # 'bank_info': json.dumps(bank_info),
        'bank_info': json.dumps(banks, cls=DjangoJSONEncoder),
        'credit_card': json.dumps(ccs, cls=DjangoJSONEncoder),
        'bank_lines': json.dumps(bank_lines, cls=DjangoJSONEncoder),
        'cc_lines': json.dumps(cc_lines, cls=DjangoJSONEncoder),
        'cc_pays': json.dumps(cc_pays, cls=DjangoJSONEncoder),
        'data': data,
        'json_data': json.dumps(json_data),
        # 'line_items': output,
        'type': output[0]
        # 'expenses': json.dumps(expenses)
    }
    # logger.exception("Bad Request 404")
    # return HttpResponseBadRequest("404")
    raise Exception('Make response code 500!')
    return render(request, 'pages/d3_test.html', context)


# main function to upload latest line items/categories/accounts
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
        elif upload_type == 'pay_cc':
            upload_name = 'Credit Card Payment'
            form = UploadCreditCardPaymentForm(request.POST)
        else:
            upload_name = 'Line Item'
            form = UploadLineItemForm(request.POST)

        # check whether it's valid:
        if form.is_valid():

            # check if it's expense or revenue line item
            if upload_type == 'expense':
                # expense then get corresponding bank/cc form
                exp_data = get_exp_data(request.POST)
                if request.POST['pay_type'] == 'cash' or request.POST['pay_type'] == 'debit':
                    form2 = UploadBankLineItemForm(exp_data)
                else:
                    form2 = UploadCreditCardLineItemForm(exp_data)

                if form2.is_valid():
                    # proceed to edit the appropriate account!
                    update_bank_exp(exp_data, request.POST['pay_type'])
                    form2.save()
                else:
                    HttpResponse('<h1>Bank Line Item Form error</h1>')
            elif upload_type == 'revenue':
                # revenue then get rev data then submit bank form
                rev_data = get_rev_data(request.POST)
                # return HttpResponse('<p>' + str(rev_data) + '</p><p>' + request.POST['category'] + '</p>')
                form2 = UploadBankLineItemForm(rev_data)

                if form2.is_valid():
                    # proceed to edit the bank accounts!
                    update_bank_rev(rev_data)
                    form2.save()
                else:
                    HttpResponse('<h1>Bank Line Item Form error</h1>')
            elif upload_type == 'pay_cc':
                credit_card_payment(request.POST)
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
        elif upload_type == 'pay_cc':
            upload_name = 'Credit Card Payment'
            form = UploadCreditCardPaymentForm()
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
    elif upload_type == 'pay_cc':
        upload_name = 'Credit Card Payment'
        item = CreditCardPayment.objects.latest('pk')
    else:
        upload_name = 'Line Item'
        item = LineItem.objects.latest('pk')

    context = {
        'upload_type': upload_type,
        'upload_name': upload_name,
        'item': item
    }
    return render(request, 'pages/upload_done.html', context)
