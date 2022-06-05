from django.urls import path

from .views import *

app_name = 'customers'
urlpatterns = [
    path('',customer_list_view,name='index'),
    path('<int:pk>/',customer_detail_update_view,name='detail_update'),
    path('<int:pk>/delete/',customer_delete_view,name='delete'),
    path('create/',customer_create_view,name='create'),
    path('membership/<int:pk>/delete/',membership_delete_view,name='ms_delete'),
]
