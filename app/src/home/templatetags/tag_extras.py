from django import template
register = template.Library()

from django.utils.html import format_html

from employees.models import *
from employees.forms import *


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
def main_ctn(extra_classes = ""):
    return format_html(
        f'<div class="container {extra_classes}" style="max-width:900px">'
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
    trips = bus_staff.trips.order_by('-departure_time')
    return {'trips':trips}