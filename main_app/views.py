from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DetailView
from django.views.generic.edit import UpdateView
from .forms import CheckoutForm, EditAddressForm, PaymentForm
from .models import Art, Cart, Order, Address, Payment
import os
import stripe
import json
from flask import Flask
stripe.api_key = os.environ['STRIPE_SECRET_KEY']


# Create your views here.


def about(request):
    return render(request, 'about.html')


def arts_index(request):
    arts = Art.objects.all()
    return render(request, 'art/index.html', {'arts': arts})


def art_detail(request, art_id):
    art = Art.objects.get(id=art_id)
    return render(request, 'art/detail.html', {'art': art})


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


@login_required
def cart_index(request):
    order = []
    cart = Cart.objects.filter(user=request.user)
    address = Address.objects.filter(user=request.user)
    try:
        order = Order.objects.get(user=request.user, ordered=False)
    except:
        pass
    return render(request, 'cart/index.html', {
        'cart': cart,
        'order': order,
        'address': address, 
        'user': request.user
        })


@login_required
def add_cart(request, art_id):
    cart_item, created = Cart.objects.get_or_create(
        art=Art.objects.get(id=art_id),
        user=request.user,
    )
    order = Order.objects.filter(user=request.user, ordered=False)
    if order.exists():
        order = order[0]
        if order.art.filter(art_id=art_id).exists():
            messages.info(request, "This item is already in your cart.")
            return redirect('cart_index')
        else:
            order.art.add(cart_item)
            messages.info(request, "This item was added to your cart.")
            return redirect('cart_index')
    else:
        order = Order.objects.create(user=request.user)
        order.art.add(cart_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('cart_index')


@login_required
def delete_cart(request):
    Order.objects.filter(user=request.user, ordered=False).delete()
    Cart.objects.filter(user=request.user, ordered=False).delete()
    return redirect('cart_index')


@login_required
def delete_cart_item(request, art_id):
    Order.objects.filter(user=request.user, ordered=False, art=art_id).delete()
    Cart.objects.filter(user=request.user, art_id=art_id).delete()
    return redirect('cart_index')

class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    template = 'main_app/order_detail.html'

class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }

            return render(self.request, 'main_app/checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect('checkout')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                shipping_address1 = form.cleaned_data.get(
                    'shipping_address')
                shipping_address2 = form.cleaned_data.get(
                    'shipping_address2')
                shipping_country = form.cleaned_data.get(
                    'shipping_country')
                shipping_zip = form.cleaned_data.get(
                    'shipping_zip')

                if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                    try:
                        shipping_address = Address.objects.get(
                            user=self.request.user,
                            address_type='S'
                            )
                    except Address.DoesNotExist:
                        shipping_address = None

                    if shipping_address is not None:
                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')

                        if set_default_shipping:
                            shipping_address.street_address=shipping_address1
                            shipping_address.apartment_address=shipping_address2
                            shipping_address.country=shipping_country
                            shipping_address.zip=shipping_zip

                    else:
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                            )
                        
                    shipping_address.save()
                    order.shipping_address = shipping_address
                    order.save()

                    same_billing_address = form.cleaned_data.get(
                        'same_billing_address')

                    if same_billing_address:
                        billing_address = shipping_address
                        billing_address.pk = None
                        billing_address.address_type = 'B'
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()
                    else:
                        billing_address1 = form.cleaned_data.get(
                            'billing_address')
                        billing_address2 = form.cleaned_data.get(
                            'billing_address2')
                        billing_country = form.cleaned_data.get(
                            'billing_country')
                        billing_zip = form.cleaned_data.get(
                            'billing_zip')
                            
                        if is_valid_form([billing_address1, billing_country, billing_zip]):
                            try:
                                billing_address = Address.objects.get(
                                    user=self.request.user,
                                    address_type='B'
                                    )
                            except Address.DoesNotExist:
                                billing_address = None

                            if billing_address is not None:
                                set_default_billing = form.cleaned_data.get(
                                    'set_default_billing')

                                if set_default_billing:
                                    billing_address.street_address=billing_address1
                                    billing_address.apartment_address=billing_address2
                                    billing_address.country=billing_country
                                    billing_address.zip=billing_zip

                            else:
                                billing_address = Address(
                                    user=self.request.user,
                                    street_address=billing_address1,
                                    apartment_address=billing_address2,
                                    country=billing_country,
                                    zip=billing_zip,
                                    address_type='B'
                                    )
                                
                            billing_address.save()
                            order.billing_address = billing_address
                            order.save()
                        else:
                            messages.info(
                                self.request, "Please fill in the required billing address fields")
                else:
                    messages.info(
                        self.request, "Please fill in the required shipping address fields")

                return redirect('payment')

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('cart_index')


class PaymentView(View):
    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = os.environ.STRIPE_PUBLISHABLE_KEY
        return context

    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
            }
            

            return render(self.request, 'main_app/payment.html', context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect('checkout')

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)

        if form.is_valid():
            # token = form.cleaned_data.get('stripeToken')
            token = form.data.get['stripeToken']
            amount = int(order.get_total_price() * 100)

            try:
                customer = stripe.Customer.create(description='test', source=token)
                charge = stripe.Charge.create(
                        amount=amount,
                        currency="usd",
                        source=request.POST['stripeToken']
                    )

                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total_price()
                payment.save()


                order_items = order.art.all()
                order_items.update(ordered=True)
                for art in order_items:
                    art.save()

                order.ordered = True
                order.payment = payment
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect('order_detail')

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                print('stripCardError', e)
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("cart_index")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                print('rate', e)
                messages.warning(self.request, "Rate limit error")
                return redirect("cart_index")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print('invalidrequest', e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("cart_index")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                print('auth', e)
                messages.warning(self.request, "Not authenticated")
                return redirect("cart_index")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                print('api', e)
                messages.warning(self.request, "Network error")
                return redirect("cart_index")
        messages.warning(self.request, "Invalid data received")
        return redirect('payment')

class UpdateAddress(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            address_type = self.request.GET.get('type')

            try:
                address = Address.objects.get(
                    user=self.request.user,
                    address_type=address_type
                )
            except Address.DoesNotExist:
                address = None

            form = EditAddressForm()
            if address is not None:
                form.fields['country'].initial = address.country

            context = {
                'form': form,
                'address': address,
            }

            context.update({'address_type': address_type})

            return render(self.request, 'main_app/address.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect('checkout')

    def post(self, *args, **kwargs):
        address_type = self.request.GET.get('type')

        form = EditAddressForm(self.request.POST)
        try:
            if form.is_valid():
                address1 = form.cleaned_data.get(
                    'address1')
                address2 = form.cleaned_data.get(
                    'address2')
                country = form.cleaned_data.get(
                    'country')
                zip = form.cleaned_data.get(
                    'zip')

                if is_valid_form([address1, country, zip]):
                    try:
                        address = Address.objects.get(
                            user=self.request.user,
                            address_type=address_type
                            )
                    except Address.DoesNotExist:
                        address = None

                    if address is not None:
                        address.street_address=address1
                        address.apartment_address=address2
                        address.country=country
                        address.zip=zip
                    else:
                        address = Address(
                            user=self.request.user,
                            street_address=address1,
                            apartment_address=address2,
                            country=country,
                            zip=zip,
                            address_type=address_type
                        )

                    address.save()
                        
                else:
                    messages.info(
                        self.request, "Please fill in the required shipping address fields")

                return redirect('cart_index')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('cart_index')

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
