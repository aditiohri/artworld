from django.urls import path
from . import views

urlpatterns = [
    path('', views.arts_index, name='index'),
]