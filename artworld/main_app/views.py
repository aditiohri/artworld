from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Art

# Create your views here.

def arts_index(request):
    arts = Art.objects.all()
    return render(request, 'index.html', { 'arts': arts })

class ArtList(ListView):
    model = Art
    fields = '__all__'
    success_url = '/art/'
    template_name = 'art.html'
