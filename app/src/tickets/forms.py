from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Row,Column,Submit,Button
from crispy_forms.bootstrap import InlineRadios,FormActions

from .models import *


class TicketForm(forms.ModelForm):
    total_cost = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={'readonly':True}
        )
    )

    def __init__(self,*args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()


class PassengerTicketForm(TicketForm):
    class Meta:
        model = PassengerTicket
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super(PassengerTicketForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(Column('trip')),
            Row(Column('paid')),
            Row(Column('customer'),Column('program')),
            Row(Column('total_cost'),Column('seat_num'),Column('payment_method')),
            Row(Column('start_location')),
            FormActions(
                Submit('save','Save'),
                css_class='d-grid gap-2 d-flex justify-content-end'
            )
        )
        self.fields['trip'].disabled = True

class LuggageTicketForm(TicketForm):
    class Meta:
        model = LuggageTicket
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super(LuggageTicketForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(Column('trip')),
            Row(Column('paid')),
            Row(Column('customer'),Column('program')),
            Row(Column('total_cost'),Column('weight'),Column('payment_method')),
            Row(Column('description')),
            Row(Column('start_location')),
            FormActions(
                Submit('save','Save'),
                css_class='d-grid gap-2 d-flex justify-content-end'
            )
        )
        self.fields['trip'].disabled = True


# class PassengerTicketCreateForm(PassengerTicketForm):
#     def __init__(self,*args, **kwargs):
#         super(PassengerTicketCreateForm,self).__init__(*args, **kwargs)
#         self.fields['trip'].disabled = True


# class LuggageTicketCreateForm(LuggageTicketForm):
#     def __init__(self,*args, **kwargs):
#         super(LuggageTicketCreateForm,self).__init__(*args, **kwargs)
#         self.fields['trip'].disabled = True
