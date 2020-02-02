from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import LineItem, Category
from .forms import UploadLineItemForm, UploadCategoryForm


# Create your views here.
def show_data(request):
    items = LineItem.objects.all()

    context = {
        'line_items': items
    }
    return render(request, 'pages/display.html', context)


def upload_data(request, upload_type):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        if upload_type == 'line_item':
            form = UploadLineItemForm(request.POST)

            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                form.save()
                # redirect to a new URL:
                return HttpResponseRedirect('/upload_done/line_item/')
        else:
            form = UploadCategoryForm(request.POST)

            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                form.save()
                # redirect to a new URL:
                return HttpResponseRedirect('/upload_done/category/')

    # if a GET (or any other method) we'll create a blank form
    else:
        if upload_type == 'line_item':
            form = UploadLineItemForm()
        else:
            form = UploadCategoryForm()

    context = {
        'form': form,
        'upload_type': upload_type
    }

    return render(request, 'pages/upload.html', context)


def upload_done(request, upload_type):
    if upload_type == 'line_item':
        upload_name = 'Line Item'
        item = LineItem.objects.latest('pk')
    else:
        upload_name = 'Category'
        item = Category.objects.latest('pk')
    context = {
        'upload_type': upload_type,
        'upload_name': upload_name,
        'item': item
    }
    return render(request, 'pages/upload_done.html', context)
