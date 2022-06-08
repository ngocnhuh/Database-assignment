from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView,DeleteView,CreateView

from .models import *
from .forms import *


class TicketDetailUpdateView(UpdateView):
    template_name = 'tickets/ticket_du_view.html'
    pk_field = 'ticket_id'

    def get_object(self):
        ticket = get_object_or_404(Ticket,ticket_id=self.kwargs.get('pk'))
        return ticket.get_child()

    def get_form_class(self):
        obj = self.get_object()
        if isinstance(obj,PassengerTicket):
            return PassengerTicketFreezeForm
        elif isinstance(obj,LuggageTicket):
            return LuggageTicketFreezeForm
        return None

    def get_success_url(self):
        return reverse_lazy(
            'tickets:ticket_detail_update',
            kwargs={'pk':self.get_object().ticket_id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket"] = self.get_object()
        return context
ticket_detail_update_view = TicketDetailUpdateView.as_view()


class PassengerTicketCreateView(CreateView):
    model = PassengerTicket
    form_class = PassengerTicketForm
    template_name = 'tickets/ticket_c_view.html'

    def get_initial(self):
        trip_id = self.request.GET.get('trip_id')
        trip = get_object_or_404(Trip,trip_id=trip_id)

        initial = {}
        initial['trip'] = trip
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket_type"] = 'Passenger Ticket'
        context["trip_id"] = self.request.GET.get('trip_id')
        return context
    
    def get_success_url(self):
        return reverse_lazy(
            'trips:trip_detail_update',
            kwargs={'pk':self.request.GET.get('trip_id')}
        )
passenger_ticket_create_view = PassengerTicketCreateView.as_view()


class LuggageTicketCreateView(CreateView):
    model = LuggageTicket
    form_class = LuggageTicketForm
    template_name = 'tickets/ticket_c_view.html'

    def get_initial(self):
        trip_id = self.request.GET.get('trip_id')
        trip = get_object_or_404(Trip,trip_id=trip_id)

        initial = {}
        initial['trip'] = trip
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket_type"] = 'Luggage Ticket'
        context["trip_id"] = self.request.GET.get('trip_id')
        return context
    
    def get_success_url(self):
        return reverse_lazy(
            'trips:trip_detail_update',
            kwargs={'pk':self.request.GET.get('trip_id')}
        )
luggage_ticket_create_view = LuggageTicketCreateView.as_view()


class TicketDeleteView(DeleteView):
    model = Ticket
    pk_field = 'ticket_id'
    template_name = 'tickets/ticket_d_view.html'

    def get_success_url(self):
        return reverse_lazy(
            'trips:trip_detail_update',
            kwargs={'pk':self.get_object().trip.trip_id}
        )
ticket_delete_view = TicketDeleteView.as_view()
