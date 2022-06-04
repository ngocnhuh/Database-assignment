from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views import View

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


def get_emp_form(request,instance,job_type):
    if job_type == 'manager':
        return ManagerForm(request.POST or None, instance=instance)
    if job_type == 'driver':
        return DriverForm(request.POST or None, instance=instance)
    if job_type == 'bus staff':
        return BusStaffForm(request.POST or None, instance=instance)
    if job_type == 'telephone staff':
        return TelephoneStaffForm(request.POST or None, instance=instance)