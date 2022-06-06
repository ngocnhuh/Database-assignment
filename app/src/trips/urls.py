from django.urls import path

from .views import *

app_name = 'trips'
urlpatterns = [
    path('',trip_search_view,name='trip_search'),
    path('<int:pk>/du/',trip_detail_update_view,name='trip_detail_update'),
    path('create/',trip_create_view,name='trip_create'),
    path('<int:pk>/delete/',trip_delete_view,name='trip_delete'),

    path('bus/',bus_list_view,name='bus_list'),
    path('bus/<str:slug>/du/',bus_detail_update_view,name='bus_detail_update'),
    path('bus/create/',bus_create_view,name='bus_create'),
    path('bus/<str:slug>/delete/',bus_delete_view,name='bus_delete'),

    path('route/',route_list_view,name='route_list'),
    path('route/<int:pk>/du/',route_detail_update_view,name='route_detail_update'),
    path('route/create/',route_create_view,name='route_create'),
    path('route/<int:pk>/delete/',route_delete_view,name='route_delete'),

    path('schedule/',sched_list_view,name='sched_list'),
    path('schedule/<int:pk>/du/',sched_detail_update_view,name='sched_detail_update'),
    path('schedule/create/',sched_create_view,name='sched_create'),
    path('schedule/<int:pk>/delete/',sched_delete_view,name='sched_delete'),
]
