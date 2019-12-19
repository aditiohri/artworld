from django.shortcuts import render
from django.http import HttpResponse
from .models import Art

# Create your views here.

def index(request):
    return HttpResponse("Art World Index")

def arts_index(resquest):
    arts = Art.objects.all()
    return render(request, 'arts/index.html', { 'arts': arts })
