from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def homepage(request):
    return render(request, 'homepage/index.html')
