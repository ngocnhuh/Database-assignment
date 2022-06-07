from django.urls import path

from .views import *

app_name = 'customers'
urlpatterns = [
    path('',customer_list_view,name='index'),
    path('<int:pk>/',customer_detail_update_view,name='detail_update'),
    path('<int:pk>/delete/',customer_delete_view,name='delete'),
    path('create/',customer_create_view,name='create'),

    path('membership/<int:pk>/delete/',membership_delete_view,name='ms_delete'),

    path('sale_promotion/',sale_prom_list_view,name='sale_prom_list'),
    path('sale_promotion/<int:pk>/',sale_prom_detail_update_view,name='sale_prom_detail_update'),
    path('sale_promotion/create/',sale_prom_create_view,name='sale_prom_create'),
    path('sale_promotion/<int:pk>/delete/',sale_prom_delete_view,name='sale_prom_delete'),

]
