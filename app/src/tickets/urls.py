from django.urls import path

from .views import *

app_name = 'tickets'
urlpatterns = [
    path('<int:pk>/du/',ticket_detail_update_view,name='ticket_detail_update'),
    path('passenger_ticket/create',passenger_ticket_create_view,name='passenger_ticket_create'),
    path('luggage_ticket/create',luggage_ticket_create_view,name='luggage_ticket_create'),
    path('<int:pk>/delete',ticket_delete_view,name='ticket_delete'),
]
