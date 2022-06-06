from django.shortcuts import render

from rest_framework.generics import ListAPIView

from .serializers import TripSerializer
from trips.models import Trip

from django.db.models import Q

from datetime import datetime

class TripSearchListAPIView(ListAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_queryset(self):
        qs = super(TripSearchListAPIView,self).get_queryset()

        route_start = self.request.GET.get('route_start') or None
        route_dest = self.request.GET.get('route_dest') or None
        date = self.request.GET.get('date') or None

        if route_start is not None:
            qs = qs.filter(sched__route__starting_point = route_start)
        if route_dest is not None:
            qs = qs.filter(sched__route__destination = route_dest)
        if date is not None:
            date = datetime.strptime(date,'%Y-%m-%d').date()
            qs = qs.filter(departure_date__gte = date)

        return qs

trip_search_list_api_view = TripSearchListAPIView.as_view()