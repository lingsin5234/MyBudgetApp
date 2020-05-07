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
from djangoapps.utils import get_this_template
from .reconcile import reconcile_bank_balances, pd_reconcile_bank_balances
# from .plotly import budget_demo
import datetime as dt
from .data_generator import generate_budget_data

# create logger instance
# logger = logging.getLogger(__name__)


# project page
def project_markdown(request):

    page_height = 1050
    f = open('budget/README.md', 'r')
    if f.mode == 'r':
        readme = f.read()
        page_height = len(readme) - 350

    content = {
        'readme': readme,
        'page_height': page_height
    }

    template_page = get_this_template('budget', 'project.html')

    return render(request, template_page, content)


# line item test view
def show_data(request):
    exps = ExpenseLineItem.objects.all().order_by('-date_stamp')
    exp_cat = ExpCategory.objects.all()
    revs = RevenueLineItem.objects.all().order_by('-date_stamp')
    rev_cat = RevCategory.objects.all()

    exp_cats = []
    for e in exp_cat:
        add = model_to_dict(e)
        exp_cats.append(add)

    rev_cats = []
    for e in rev_cat:
        add = model_to_dict(e)
        rev_cats.append(add)

    expense = []
    for i in exps:
        add = model_to_dict(i)
        cat_index = add['category']
        add['category'] = exp_cats[cat_index]['name']
        expense.append(add)

    revenue = []
    for i in revs:
        add = model_to_dict(i)
        cat_index = add['category']
        add['category'] = rev_cats[cat_index]['name']
        revenue.append(add)

    context = {
        'expense': json.dumps(expense, cls=DjangoJSONEncoder),
        'revenue': json.dumps(revenue, cls=DjangoJSONEncoder)
    }
    return render(request, 'pages/display.html', context)


# d3.js test view
def show_d3(request):

    # convert all objects from dict_to_model
    bank = BankAccount.objects.all()
    cc = CreditCard.objects.all()
    bank_line = BankLineItem.objects.all().order_by('-date_stamp')
    cc_line = CreditCardLineItem.objects.all().order_by('-date_stamp')
    cc_pay = CreditCardPayment.objects.all().order_by('-date_stamp')

    banks = []
    ccs = []
    bank_lines = []
    cc_lines = []
    cc_pays = []

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
        'bank_info': json.dumps(banks, cls=DjangoJSONEncoder),
        'credit_card': json.dumps(ccs, cls=DjangoJSONEncoder),
        'bank_lines': json.dumps(bank_lines, cls=DjangoJSONEncoder),
        'cc_lines': json.dumps(cc_lines, cls=DjangoJSONEncoder),
        'cc_pays': json.dumps(cc_pays, cls=DjangoJSONEncoder)
    }
    return render(request, 'pages/dashboard.html', context)


# dashboard version 2
def show_dashboard(request):

    # convert all objects from dict_to_model
    bank = BankAccount.objects.all()
    cc = CreditCard.objects.all()
    bank_line = BankLineItem.objects.all().order_by('-date_stamp')
    cc_line = CreditCardLineItem.objects.all().order_by('-date_stamp')
    cc_pay = CreditCardPayment.objects.all().order_by('-date_stamp')

    banks = []
    ccs = []
    bank_lines = []
    cc_lines = []
    cc_pays = []

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

    # recapture the previous values
    # print("Views output: ", reconcile_bank_balances(banks, bank_lines, cc_pays, 10))
    balances = reconcile_bank_balances(banks, bank_lines, cc_pays, 10)

    context = {
        'bank_info': json.dumps(banks, cls=DjangoJSONEncoder),
        'credit_card': json.dumps(ccs, cls=DjangoJSONEncoder),
        'bank_lines': json.dumps(bank_lines, cls=DjangoJSONEncoder),
        'cc_lines': json.dumps(cc_lines, cls=DjangoJSONEncoder),
        'cc_pays': json.dumps(cc_pays, cls=DjangoJSONEncoder),
        'balances': json.dumps(balances, cls=DjangoJSONEncoder)
    }

    return render(request, 'pages/budget_dashboard.html', context)


# main function to upload latest line items/categories/accounts
def upload_data(request, upload_type):
    # default upload_name
    upload_name = 'Expense Item'

    try:
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            if upload_type == 'expense':
                try:
                    form = UploadExpenseForm(request.POST)
                except Exception as exp:
                    logging.error(exp)
                    return HttpResponse(exp, status=400)
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

    except Exception as exp:
        logging.error(exp)
        return HttpResponse(exp, status=400)

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


# show the categories
def show_category(request, cat_type):

    # either revenue or expense
    if cat_type == 'revenue':
        cat = RevCategory.objects.all()
    else:
        cat = ExpCategory.objects.all()

    # convert to dict to use JSON
    cats = []
    for c in cat:
        add = model_to_dict(c)
        cats.append(add)

    context = {
        'cats': json.dumps(cats),
        'cat_type': cat_type
    }
    return render(request, 'pages/show_cats.html', context)


# Dashboard Plotly
def show_plotly_dash(request):

    '''
    # convert all objects from dict_to_model
    bank = BankAccount.objects.values_list()
    cc = CreditCard.objects.values_list()
    bank_line = BankLineItem.objects.values_list().order_by('-date_stamp')
    cc_line = CreditCardLineItem.objects.values_list().order_by('-date_stamp')
    cc_pay = CreditCardPayment.objects.values_list().order_by('-date_stamp')

    bank_col = BankAccount._meta.fields
    cc_col = CreditCard._meta.fields
    bl_col = BankLineItem._meta.fields
    cl_col = CreditCardLineItem._meta.fields
    cp_col = CreditCardPayment._meta.fields

    pd_reconcile_bank_balances(bank, bank_col, bank_line, bl_col, cc_pay, cp_col)
    '''

    return render(request, 'pages/budget_plotly.html')


# Generate BUDGET Data
def budget_data_generate(request):

    # generate data
    s_date = dt.datetime(2019, 1, 4)
    e_date = dt.datetime(2020, 5, 1)
    # generate_budget_data(s_date, e_date)
    # print(json.dumps(generate_budget_data(s_date, e_date), cls=DjangoJSONEncoder, indent=4))
    # '''
    with open('budget_READY20200506.json', 'w') as outfile:
        json.dump(generate_budget_data(s_date, e_date), outfile, cls=DjangoJSONEncoder, indent=4)
    # '''
    return render(request, 'pages/budget_data-gen.html')