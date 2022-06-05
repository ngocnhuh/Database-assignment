from django.urls import path

from .views import *

app_name = 'trips'
urlpatterns = [
    path('bus/',bus_list_view,name='bus_list'),
    path('bus/<str:slug>/du/',bus_detail_update_view,name='bus_detail_update'),
    path('bus/create/',bus_create_view,name='bus_create'),
    path('bus/<str:slug>/delete/',bus_delete_view,name='bus_delete'),

    path('route/',route_list_view,name='route_list'),
    path('route/<int:pk>/du/',route_detail_update_view,name='route_detail_update'),
    path('route/create/',route_create_view,name='route_create'),
    path('route/<int:pk>/delete/',route_delete_view,name='route_delete'),
]
