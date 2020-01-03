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
    path('address/update', views.UpdateAddress.as_view(), name='update_address'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('order/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
]