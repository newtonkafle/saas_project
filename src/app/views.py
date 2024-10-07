from django.http import HttpResponse
from visits.models import PageVisits
import pathlib
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings


LOGIN_URL = settings.LOGIN_URL
this_dir = pathlib.Path(__file__).resolve().parent

def home_page_view(request, *args, **kwargs):
    print(this_dir)
    PageVisits.objects.create()
    return render(request, 'home.html')

# this is an comment 


def looks_good(self):
    print("hey I'm looking good")

VALID_CODE = 'ass'

def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0
    if request.method == "POST":
        user_code = request.POST.get('code') or None
        if user_code == VALID_CODE:
            request.session['protected_page_allowed'] = 1
    if is_allowed:
        return render(request, 'protected/view.html', {})
    return render(request, "protected/entry.html", {})

@login_required
def user_only_view(request, *args, **kwargs):
   # if request.user.is_staff:

    return render(request, "protected/user-only.html", {})

@staff_member_required(login_url=LOGIN_URL)
def staff_only_view(request, *args, **kwargs):
    return render(request, "protected/user-only.html")