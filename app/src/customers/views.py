from django.urls import reverse_lazy
from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from django.views.generic import CreateView,DeleteView
from django.http import HttpResponse

from .models import *
from .forms import *

class CustomerListView(View):
    def get(self,request):
        customers = Customer.objects.all()
        ctx = {
            'customers':customers
        }
        return render(request, 'customers/index.html', ctx)

customer_list_view = CustomerListView.as_view()


class CustomerDetailUpdateView(View):
    def get(self,request,pk):
        cus = get_object_or_404(Customer,customer_id=pk)
        form = CustomerForm(instance=cus)

        ctx = {
            'has_ms': False,
            'cus_id': cus.customer_id,
            'form': form
        }

        if hasattr(cus, 'membership'):
            membership = cus.membership
            ctx['has_ms'] = True
            ctx['ms_id'] = cus.membership.member_id
            ctx['ms_form'] = MembershipForm(instance=membership)
        else:
            ctx['ms_form'] = MembershipForm()


        return render(request, 'customers/cus_du_view.html',ctx)

    def post(self,request,pk):
        cus = get_object_or_404(Customer,customer_id=pk)

        ctx = {
            'has_ms': False,
            'cus_id': cus.customer_id,
        }

        cus_form = None
        ms_form = None

        if 'ms-save-btn' in request.POST:
            cus_form = CustomerForm(instance=cus)
            if hasattr(cus, 'membership'):
                ms_form = MembershipForm(request.POST,instance=cus.membership)
            else:
                ms_form = MembershipForm(request.POST)
            if ms_form.is_valid():
                ms = ms_form.save(commit=False)
                ms.customer = cus
                ms.save()

        elif 'cus-save-btn' in request.POST:
            cus_form = CustomerForm(request.POST,instance=cus)
            if cus_form.is_valid():
                cus_form.save()
            if hasattr(cus, 'membership'):
                ms_form = MembershipForm(instance=cus.membership)
            else:
                ms_form = MembershipForm()

        ctx['form'] = cus_form
        ctx['ms_form'] = ms_form

        if hasattr(cus, 'membership'):
            ctx['ms_id'] = cus.membership.member_id
            ctx['has_ms'] = True
        
        return render(request, 'customers/cus_du_view.html',ctx)

customer_detail_update_view = CustomerDetailUpdateView.as_view()


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customers:index')
    template_name = 'customers/cus_c_view.html'

customer_create_view = CustomerCreateView.as_view()


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers:index')
    template_name = 'customers/cus_d_view.html'

customer_delete_view = CustomerDeleteView.as_view()


class MembershipDeleteView(DeleteView):
    model = Membership
    template_name = 'customers/ms_d_view.html'

    def get_success_url(self,**kwargs):
        return reverse_lazy('customers:detail_update',
            kwargs={'pk':self.object.customer.customer_id})

membership_delete_view = MembershipDeleteView.as_view()
