from django.urls import path

from .views import *

app_name = 'employees'
urlpatterns = [
    path('',employee_list_view,name='index'),
    path('<int:pk>/',employee_detail_update_view,name='detail'),

    path('manager/create/',manager_create_view,name='manager_create'),
    path('driver/create/',driver_create_view,name='driver_create'),
    path('bus_staff/create/',bus_staff_create_view,name='bus_staff_create'),
    path('telephone_staff/create/',telephone_staff_create_view,name='telephone_staff_create'),

    path('employee/<int:pk>/delete',employee_delete_view,name='delete'),
]