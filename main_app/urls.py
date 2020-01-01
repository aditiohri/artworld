from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.arts_index, name='index'),
    path('arts/<int:art_id>/', views.art_detail, name='detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('cart/', views.cart_index, name='cart_index'),
    path('cart/<int:art_id>/add_cart/', views.add_cart, name='add_cart'), 
    path('cart/delete', views.delete_cart, name='delete_cart'),
    path('cart/<int:art_id>/delete', views.delete_cart_item, name='delete_cart_item'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order/<int:pk>/update', views.OrderView.as_view(), name='address_update'),
    # path('payment/<payment_option>/', views.PaymentView.as_view(), name='payment')
]