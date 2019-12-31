from django.contrib import admin
from .models import Art, Cart, Order, Address, Payment

# Register your models here.
admin.site.register(Art)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Payment)
