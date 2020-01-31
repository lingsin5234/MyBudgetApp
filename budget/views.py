from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import LineItem
from .forms import UploadDataForm


# Create your views here.
def show_data(request):
    items = LineItem.objects.all()

    context = {
        'line_items': items
    }
    return render(request, 'pages/display.html', context)


def upload_data(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UploadDataForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/upload_done/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadDataForm()

    return render(request, 'pages/upload.html', {'form': form})


def upload_done(request):
    item = LineItem.objects.latest('pk')
    context = {'line_item': item}
    return render(request, 'pages/upload_done.html', context)
