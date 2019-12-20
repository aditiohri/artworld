from django.urls import path
from . import views
# from main_app.views import ArtList

urlpatterns = [
    path('', views.arts_index, name='index'),
    # path('art/', ArtList.as_view()),
    path('accounts/signup/', views.signup, name='signup'),
    path('arts/<int:art_id>/', views.arts_detail, name='detail'),
]