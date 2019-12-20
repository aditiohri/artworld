from django.urls import path
from . import views
# from main_app.views import ArtList

urlpatterns = [
    path('', views.arts_index, name='index'),
    # path('art/', ArtList.as_view()),
    path('accounts/signup/', views.signup, name='signup'),
    path('arts/<int:art_id>/', views.art_detail, name='detail'),
    path('orders/', views.orders_index, name='order_index'),
    path('orders/<int:art_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/add_order/', views.add_order, name='add_order'),
]