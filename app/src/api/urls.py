from django.urls import path

from .views import trip_search_list_api_view

app_name = 'api'
urlpatterns = [
    path('trips/search/',trip_search_list_api_view,name='trip_search_api')
]
