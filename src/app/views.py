from django.http import HttpResponse
from visits.models import PageVisits
import pathlib
from django.shortcuts import render


this_dir = pathlib.Path(__file__).resolve().parent

def home_page_view(request, *args, **kwargs):
    print(this_dir)
    PageVisits.objects.create()
    return render(request, 'home.html')

# this is an comment 


def looks_good(self):
    print("hey I'm looking good")