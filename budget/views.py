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
            print(request.POST)
            form = UploadLineItemForm(request.POST)

            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                form.save()
                # redirect to a new URL:
                return HttpResponseRedirect('/upload_done/line_item/')
        else:
            print("HELLO?")
            print(request.POST)
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
            print("First")
            form = UploadCategoryForm()

    return render(request, 'pages/upload.html', {'form': form})


def upload_done(request, upload_type):
    if upload_type == 'line_item':
        item = LineItem.objects.latest('pk')
    else:
        item = Category.objects.latest('pk')
    context = {
        'upload_type': upload_type,
        'item': item
    }
    return render(request, 'pages/upload_done.html', context)
