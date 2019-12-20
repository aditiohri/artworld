from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Art
from .forms import OrderForm

# Create your views here.

def arts_index(request):
    arts = Art.objects.all()
    return render(request, '.../index.html', { 'arts': arts })

# class ArtList(ListView):
#     model = Art
#     fields = '__all__'
#     success_url = '/art/'
#     context_object_name = 'artwork'
#     template_name = 'art.html'

def art_detail(request, art_id):
  art = Art.objects.get(id=art_id)
  order_form = OrderForm()
  return render(request, '.../detail.html', { 
      'art': art
      'order_form': order_form 
      })

def orders_index(request):
    orders = Order.objects.all()
    return render(request, '.../index.html', { 'orders': orders })  

def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, '.../detail.html', { 'order': order }))

def add_order(request, art_id):
  form = OrderForm(request.POST)
  if form.is_valid():
    new_order = form.save(commit=False)
    new_order.art_id = art_id
    new_order.save()
  return redirect('...', art_id=art_id)  

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)    
