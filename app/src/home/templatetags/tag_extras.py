from django import template
register = template.Library()

from django.utils.html import format_html

from employees.models import *
from employees.forms import *

from customers.models import *
from trips.models import Route,Trip

@register.filter
def date_decode(value):
    date_dict = {
        'MON':'Monday',
        'TUE':'Tuesday',
        'WED':'Wednesday',
        'THU':'Thursday',
        'FRI':'Friday',
        'SAT':'Saturday',
        'SUN':'Sunday',
    }
    return date_dict.get(value,value)



@register.simple_tag()
def main_ctn(extra_classes = "",max_width=900):
    return format_html(
        f'<div class="container {extra_classes}" style="max-width:{max_width}px">'
    )


@register.simple_tag()
def end_main_ctn():
    return format_html('</div>')


@register.inclusion_tag("employees/emp_inline.html")
def emp_inline(manager):
    emps = Employee.objects.filter(manager_id=manager.ee_id)
    return {'emps':emps}   


@register.inclusion_tag("employees/shift_inline.html")
def shift_inline(tele_staff):
    shifts = TeleShift.objects.filter(ee=tele_staff.ee_id)
    update_forms = [TeleShiftForm(instance=s) for s in shifts]
    return {
        'ee_id':tele_staff.ee_id,
        'shifts':zip(update_forms,shifts),
        'create_form':TeleShiftForm,
    }


@register.inclusion_tag("trips/trip_inline.html")
def trip_inline(bus_staff):
    trips = bus_staff.trips.order_by('-departure_date')
    return {'trips':trips}


@register.inclusion_tag("customers/ms_level_inline.html")
def ms_level_inline():
    ms_levels = MembershipLevel.objects.all()
    
    return {
        "ms_levels": ms_levels,
    }

@register.inclusion_tag("trips/stop_inline.html")
def stop_inline(route):
    stops = route.stops.all()
    return {"stops": stops}

@register.inclusion_tag("trips/trip_search_form.html")
def trip_search_form():
    route_starts = Route.objects.values_list('starting_point',flat=True).distinct()
    route_dests = Route.objects.values_list('destination',flat=True).distinct()
    return {
        "route_starts": route_starts,
        "route_dests": route_dests
    }


@register.inclusion_tag("tickets/ticket_inline.html")
def ticket_inline(trip_id):
    trip = Trip.objects.get(trip_id=trip_id)
    tickets = trip.tickets.all()
    passenger_tickets = []
    luggage_tickets = []

    for t in tickets:
        if t.ticket_type == "passenger ticket":
            passenger_tickets.append(t.get_child())
        elif t.ticket_type == "luggage ticket":
            luggage_tickets.append(t.get_child())

    return {
        'trip':trip,
        'passenger_tickets':passenger_tickets,
        'luggage_tickets':luggage_tickets,
    }
