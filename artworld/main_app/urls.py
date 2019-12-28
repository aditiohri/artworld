from django.urls import path
from . import views
# from main_app.views import ArtList

urlpatterns = [
    path('about/', views.about, name='about'),
    path('arts/', views.arts_index, name='index'),
    path('arts/<int:art_id>/', views.art_detail, name='detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('cart/', views.cart_index, name='cart_index'),
    path('cart/<int:art_id>/add_cart/', views.add_cart, name='add_cart'), 
    path('cart/delete', views.delete_cart, name='delete_cart'),
    path('cart/<int:art_id>/delete', views.delete_cart_item, name='delete_cart_item')
]