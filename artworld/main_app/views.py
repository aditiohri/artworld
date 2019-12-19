from django.shortcuts import render
from django.http import HttpResponse
from .models import Art

# Create your views here.

def arts_index(request):
    arts = Art.objects.all()
    return render(request, 'index.html', { 'arts': arts })
