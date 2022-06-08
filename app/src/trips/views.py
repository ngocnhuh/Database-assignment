from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView,UpdateView,CreateView,DeleteView


from .models import *
from .forms import *

class BusListView(ListView):
    model = Bus
    template_name = 'trips/bus_l_view.html'
bus_list_view = BusListView.as_view()

class BusDetailUpdateView(UpdateView):
    model = Bus
    template_name = 'trips/bus_du_view.html'
    form_class = BusForm
    slug_url_kwarg = 'slug'
    slug_field = 'bus_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bus"] = self.get_object()
        return context
    
    def get_success_url(self):
        return reverse_lazy(
            'trips:bus_detail_update',
            kwargs={'slug':self.get_object().bus_id}
        )
bus_detail_update_view = BusDetailUpdateView.as_view()

class BusCreateView(CreateView):
    model = Bus
    form_class = BusCreateForm
    success_url = reverse_lazy('trips:bus_list')
    template_name = 'trips/bus_c_view.html'
bus_create_view = BusCreateView.as_view()

class BusDeleteView(DeleteView):
    model = Bus
    slug_url_kwarg = 'slug'
    slug_field = 'bus_id'
    template_name = 'trips/bus_d_view.html'
    success_url = reverse_lazy('trips:bus_list')
bus_delete_view = BusDeleteView.as_view()


class RouteListView(ListView):
    model = Route
    template_name = 'trips/route_l_view.html'
route_list_view = RouteListView.as_view()

class RouteDetailUpdateView(UpdateView):
    model = Route
    template_name = 'trips/route_du_view.html'
    form_class = RouteForm
    pk_field = 'route_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["route"] = self.get_object()
        return context
    
    def get_success_url(self):
        return reverse_lazy(
            'trips:route_detail_update',
            kwargs={'pk':self.get_object().route_id}
        )
route_detail_update_view = RouteDetailUpdateView.as_view()

class RouteCreateView(CreateView):
    model = Route
    form_class = RouteForm
    success_url = reverse_lazy('trips:route_list')
    template_name = 'trips/route_c_view.html'
route_create_view = RouteCreateView.as_view()

class RouteDeleteView(DeleteView):
    model = Route
    pk_field = 'route_id'
    template_name = 'trips/route_d_view.html'
    success_url = reverse_lazy('trips:route_list')
route_delete_view = RouteDeleteView.as_view()


class TripScheduleListView(ListView):
    model = TripSchedule
    pk_field = 'sched_id'
    template_name = 'trips/sched_l_view.html'
sched_list_view = TripScheduleListView.as_view()

class TripScheduleDetailUpdateView(UpdateView):
    model = TripSchedule
    pk_field = 'sched_id'
    form_class = TripScheduleForm
    template_name = 'trips/sched_du_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sched"] = self.get_object()
        return context
    
    def get_success_url(self):
        return reverse_lazy(
            'trips:sched_detail_update',
            kwargs={'pk':self.get_object().sched_id}
        )
sched_detail_update_view = TripScheduleDetailUpdateView.as_view()

class TripScheduleCreateView(CreateView):
    model = TripSchedule
    form_class = TripScheduleForm
    success_url = reverse_lazy('trips:sched_list')
    template_name = 'trips/sched_c_view.html'
sched_create_view = TripScheduleCreateView.as_view()

class TripScheduleDeleteView(DeleteView):
    model = TripSchedule
    pk_field = 'sched_id'
    template_name = 'trips/sched_d_view.html'
    success_url = reverse_lazy('trips:sched_list')
sched_delete_view = TripScheduleDeleteView.as_view()


class TripSearchView(View):
    def get(self,request):
        return render(request, 'trips/trip_search.html')
trip_search_view = TripSearchView.as_view()


class TripDetailUpdateView(UpdateView):
    model = Trip
    form_class = TripDetailForm
    pk_field = 'trip_id'
    template_name = 'trips/trip_du_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.get_object()
        return context
    
    def get_success_url(self):
        return reverse_lazy(
            'trips:trip_detail_update',
            kwargs={'pk':self.get_object().trip_id}
        )
trip_detail_update_view = TripDetailUpdateView.as_view()


class TripCreateView(CreateView):
    model = Trip
    form_class = TripForm
    success_url = reverse_lazy('trips:trip_search')
    template_name = 'trips/trip_c_view.html'
trip_create_view = TripCreateView.as_view()


class TripDeleteView(DeleteView):
    model = Trip
    pk_field = 'trip_id'
    template_name = 'trips/trip_d_view.html'
    success_url = reverse_lazy('trips:trip_search')
trip_delete_view = TripDeleteView.as_view()