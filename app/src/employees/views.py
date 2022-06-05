from django.urls import reverse_lazy
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
import json

from .models import *
from .forms import *

class EmployeeListView(View):
    def get(self,request):
        employees = Employee.objects.all()

        ctx = {
            'emps': employees
        }

        return render(request,'employees/index.html', ctx)

employee_list_view = EmployeeListView.as_view()


class EmployeeDetaiUpdatelView(View):
    def get(self,request,pk):
        emp = get_object_or_404(Employee,ee_id=pk)
        sub_emp = emp.get_child()
        job_type = emp.job_type
        form = get_emp_form(request,sub_emp,job_type)

        ctx = {
            'emp': sub_emp,
            'job_type': job_type,
            'form':form
        }

        return render(request,'employees/emp_du_view.html',ctx)

    def post(self,request,pk):
        emp = get_object_or_404(Employee,ee_id=pk)
        sub_emp = emp.get_child()
        job_type = emp.job_type
        form = get_emp_form(request,sub_emp,job_type)

        if form.is_valid():
            form.save()
            
        ctx = {
            'emp': sub_emp,
            'job_type': job_type,
            'form':form
        }

        return render(request,'employees/emp_du_view.html',ctx)

employee_detail_update_view = EmployeeDetaiUpdatelView.as_view()


class ManagerCreateView(CreateView):
    model = Manager
    form_class = ManagerForm
    success_url = reverse_lazy('employees:index')
    template_name = 'employees/emp_c_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_type'] = 'Manager'
        return context

manager_create_view = ManagerCreateView.as_view()


class DriverCreateView(CreateView):
    model = Driver
    form_class = DriverForm
    success_url = reverse_lazy('employees:index')
    template_name = 'employees/emp_c_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_type'] = 'Driver'
        return context

driver_create_view = DriverCreateView.as_view()


class BusStaffCreateView(CreateView):
    model = BusStaff
    form_class = BusStaffForm
    success_url = reverse_lazy('employees:index')
    template_name = 'employees/emp_c_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_type'] = 'Bus Staff'
        return context

bus_staff_create_view = BusStaffCreateView.as_view()


class TelephoneStaffCreateView(CreateView):
    model = TelephoneStaff
    form_class = TelephoneStaffForm
    success_url = reverse_lazy('employees:index')
    template_name = 'employees/emp_c_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_type'] = 'Telephone Staff'
        return context

telephone_staff_create_view = TelephoneStaffCreateView.as_view()


def get_emp_form(request,instance,job_type):
    if job_type == 'manager':
        return ManagerForm(request.POST or None, instance=instance)
    if job_type == 'driver':
        return DriverForm(request.POST or None, instance=instance)
    if job_type == 'bus staff':
        return BusStaffForm(request.POST or None, instance=instance)
    if job_type == 'telephone staff':
        return TelephoneStaffForm(request.POST or None, instance=instance)