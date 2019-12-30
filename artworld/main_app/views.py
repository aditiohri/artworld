from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Art, Cart, Order

# Create your views here.
 
def about(request):
  return render(request, 'about.html')

def arts_index(request):
    arts = Art.objects.all()
    return render(request, 'art/index.html', { 'arts': arts })

def art_detail(request, art_id):
  art = Art.objects.get(id=art_id)
  return render(request, 'art/detail.html', { 'art': art })

@login_required
def cart_index(request):
    cart = Cart.objects.filter(user=request.user)
    return render(request, 'cart/index.html', { 'cart': cart })  

@login_required
def add_cart(request, art_id):
  new_cart_item = Cart.objects.create(
      art = Art.objects.get(id=art_id),
      user = request.user,
    )
  new_cart_item.save()
  return redirect('cart_index')  

@login_required
def delete_cart(request):
    Cart.objects.all().delete()
    return redirect('cart_index')

@login_required
def delete_cart_item(request, art_id):
    Cart.objects.filter(art_id=art_id).delete()
    return redirect('cart_index') 

def checkout(request):
  return render(request, 'checkout.html')       

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
