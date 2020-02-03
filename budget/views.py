from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import LineItem, Category, CreditCard, ExpenseLineItem
from .forms import UploadLineItemForm, UploadCategoryForm, UploadCreditCardForm, UploadExpenseForm


# line item test view
def show_data(request):
    items = LineItem.objects.all()

    context = {
        'line_items': items
    }
    return render(request, 'pages/display.html', context)


# d3.js test view
def show_d3(request):
    items = LineItem.objects.all()

    context = {
        'line_items': items
    }
    return render(request, 'pages/d3_test.html', context)


def upload_data(request, upload_type):
    # default upload_name
    upload_name = 'Expense'

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        if upload_type == 'expense':
            form = UploadExpenseForm(request.POST)
        elif upload_type == 'credit_card':
            upload_name = 'Credit Card'
            form = UploadCreditCardForm(request.POST)
        elif upload_type == 'category':
            upload_name = 'Category'
            form = UploadCategoryForm(request.POST)
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
        elif upload_type == 'category':
            upload_name = 'Category'
            form = UploadCategoryForm()
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
    if upload_type == 'line_item':
        upload_name = 'Line Item'
        item = ExpenseLineItem.objects.latest('pk')
    elif upload_type == 'credit_card':
        upload_name = 'Credit Card'
        item = CreditCard.objects.latest('pk')
    elif upload_type == 'Category':
        upload_name = 'Category'
        item = Category.objects.latest('pk')
    else:
        upload_name = 'Line Item'
        item = LineItem.objects.latest('pk')

    context = {
        'upload_type': upload_type,
        'upload_name': upload_name,
        'item': item
    }
    return render(request, 'pages/upload_done.html', context)
