from django.urls import reverse_lazy
from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from django.views.generic import CreateView,DeleteView,ListView,UpdateView
from django.http import HttpResponse
from django.db.models import F, Func
from django.db import connection,Error

from .models import *
from .forms import *

class CustomerListView(View):
    def get(self,request):
        qs = Customer.objects.all()
        qs = qs.annotate(total_money=Func(F('customer_id'),function='total_money'))
        qs = qs.order_by('-total_money')
        ctx = {
            'customers':qs
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


# class CustomerCreateView(CreateView):
#     model = Customer
#     form_class = CustomerForm
#     success_url = reverse_lazy('customers:index')
#     template_name = 'customers/cus_c_view.html'

class CustomerCreateView(View):
    def get(self,request):
        form = CustomerForm()
        return render(request,'customers/cus_c_view.html',{'form':form})
    
    def post(self,request):
        form = CustomerForm(request.POST or None)
        data = form.data

        try:
            cur = connection.cursor()
            cur.callproc("insertCustomerData", 
                [
                    data['fname'], 
                    data['lname'], 
                    data['birth_date'], 
                    data['phone'], 
                    data['address'], 
                    data['email']
                ])
            cur.close()
            return redirect(reverse_lazy('customers:index'))
        except Error as e:
            form.add_error(None, e)
            return render(request,'customers/cus_c_view.html',{'form':form})

customer_create_view = CustomerCreateView.as_view()


# class CustomerDeleteView(DeleteView):
#     model = Customer
#     success_url = reverse_lazy('customers:index')
#     template_name = 'customers/cus_d_view.html'

class CustomerDeleteView(View):
    def get(self,request,pk):
        cus = get_object_or_404(Customer,pk=pk)
        return render(request, 'customers/cus_d_view.html',{'object':cus})

    def post(self,request,pk):
        cur = connection.cursor()
        cur.callproc("deleteCustomerData",[pk])
        cur.close()
        return redirect(reverse_lazy('customers:index'))

customer_delete_view = CustomerDeleteView.as_view()


class MembershipDeleteView(DeleteView):
    model = Membership
    template_name = 'customers/ms_d_view.html'

    def get_success_url(self,**kwargs):
        return reverse_lazy('customers:detail_update',
            kwargs={'pk':self.object.customer.customer_id})

membership_delete_view = MembershipDeleteView.as_view()


class SalesPromotionListView(ListView):
    model = SalesPromotion
    template_name = 'customers/sale_prom_l_view.html'
sale_prom_list_view = SalesPromotionListView.as_view()


class SalesPromotionDetailUpdateView(UpdateView):
    model = SalesPromotion
    form_class = SalePromotionForm
    pk_field = 'program_id'
    template_name = 'customers/sale_prom_du_view.html'

    def get_success_url(self):
        return reverse_lazy(
            'customers:sale_prom_detail_update',
            kwargs={'pk':self.get_object().program_id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sale_prom"] = self.get_object()
        return context
sale_prom_detail_update_view = SalesPromotionDetailUpdateView.as_view()


class SalesPromotionCreateView(CreateView):
    model = SalesPromotion
    form_class = SalePromotionForm
    success_url = reverse_lazy('customers:sale_prom_list')
    template_name = 'customers/sale_prom_c_view.html'
sale_prom_create_view = SalesPromotionCreateView.as_view()


class SalesPromotionDeleteView(DeleteView):
    model = SalesPromotion
    pk_field = 'program_id'
    template_name = 'customers/sale_prom_d_view.html'
    success_url = reverse_lazy('customers:sale_prom_list')
sale_prom_delete_view = SalesPromotionDeleteView.as_view()