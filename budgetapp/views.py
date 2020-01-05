from django.shortcuts import render
from budgetapp.models import TestData


# Create your views here.
def upload_data(request):

    budget_data = TestData.objects.all()

    context = {
        'budget_data': budget_data
    }

    return render(request, 'pages/upload.html', context)
