from django.urls import path

from .views import *

app_name = 'employees'
urlpatterns = [
    path('',employee_list_view,name='index'),
    path('<pk>/',employee_detail_update_view,name='detail')
]