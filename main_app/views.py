from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import CheckoutForm  # , PaymentForm
from .models import Art, Cart, Order, Address, Payment  # , UserProfile

# import stripe
# stripe.api_key = settings.STRIPE_SECRET_KEY

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
        'address': address
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
        return redirect("cart_index")


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


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }

            shipping_address = Address.objects.filter(
                user=self.request.user,
                address_type='S'
            )

            if shipping_address.exists():
                context.update(
                    {'default_shipping_address': shipping_address[0]})

                billing_address = Address.objects.filter(
                user=self.request.user,
                address_type='B'
                )
            if billing_address.exists():
                context.update(
                    {'default_billing_address': billing_address[0]})

            return render(self.request, "main_app/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")

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

                return redirect('checkout')

                # payment_option = form.cleaned_data.get('payment_option')

                # if payment_option == 'S':
                #     return redirect('payment', payment_option='stripe')
                # elif payment_option == 'P':
                #     return redirect('payment', payment_option='paypal')
                # else:
                #     messages.warning(
                #         self.request, "Invalid payment option selected")
                #     return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("cart_index")


# class PaymentView(View):
#     def get(self, *args, **kwargs):
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         if order.billing_address:
#             context = {
#                 'order': order,
#             }
#             userprofile = self.request.user.userprofile
#             if userprofile.one_click_purchasing:
#                 cards = stripe.Customer.list_sources(
#                     userprofile.stripe_customer_id,
#                     limit=3,
#                     object='card'
#                 )
#                 card_list = cards['data']
#                 if len(card_list) > 0:
#                     # update the context with the default card
#                     context.update({
#                         'card': card_list[0]
#                     })
#             return render(self.request, "payment.html", context)
#         else:
#             messages.warning(
#                 self.request, "You have not added a billing address")
#             return redirect("checkout.html")

    # def post(self, *args, **kwargs):
    #     order = Order.objects.get(user=self.request.user, ordered=False)
    #     form = PaymentForm(self.request.POST)
    #     userprofile = UserProfile.objects.get(user=self.request.user)
    #     if form.is_valid():
    #         token = form.cleaned_data.get('stripeToken')
    #         save = form.cleaned_data.get('save')
    #         use_default = form.cleaned_data.get('use_default')

    #         if save:
    #             if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
    #                 customer = stripe.Customer.retrieve(
    #                     userprofile.stripe_customer_id)
    #                 customer.sources.create(source=token)

    #             else:
    #                 customer = stripe.Customer.create(
    #                     email=self.request.user.email,
    #                 )
    #                 customer.sources.create(source=token)
    #                 userprofile.stripe_customer_id = customer['id']
    #                 userprofile.one_click_purchasing = True
    #                 userprofile.save()

    #         amount = int(order.get_total() * 100)

    #         try:

    #             if use_default or save:
    #                 # charge the customer because we cannot charge the token more than once
    #                 charge = stripe.Charge.create(
    #                     amount=amount,
    #                     currency="usd",
    #                     customer=userprofile.stripe_customer_id
    #                 )
    #             else:
    #                 # charge once off on the token
    #                 charge = stripe.Charge.create(
    #                     amount=amount,
    #                     currency="usd",
    #                     source=token
    #                 )

    #             # create the payment
    #             payment = Payment()
    #             payment.stripe_charge_id = charge['id']
    #             payment.user = self.request.user
    #             payment.amount = order.get_total()
    #             payment.save()

    #             # assign the payment to the order

    #             order_items = order.items.all()
    #             order_items.update(ordered=True)
    #             for item in order_items:
    #                 item.save()

    #             order.ordered = True
    #             order.payment = payment
    #             order.ref_code = create_ref_code()
    #             order.save()

    #             messages.success(self.request, "Your order was successful!")
    #             return redirect("/")

    #         except stripe.error.StripeError as e:
    #             messages.warning(
    #                 self.request, "Something went wrong. You were not charged. Please try again.")
    #             return redirect("/")

    #     messages.warning(self.request, "Invalid data received")
    #     return redirect("/payment/stripe/")


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
