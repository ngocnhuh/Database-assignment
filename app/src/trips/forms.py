from django import forms
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Row,Column,Submit,Button
from crispy_forms.bootstrap import FormActions

from .models import *

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = '__all__'

    bus_id = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'readonly':True})
    )

    def __init__(self,*args, **kwargs):
        super(BusForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('bus_id'),Column('bustype')),
            Row(Column('total_seat'),Column('maxload'),Column('sleeper_type')),
            FormActions(
                Submit('save','Save',css_class='cus-save-btn'),
                css_class='d-grid gap-2 d-flex justify-content-end'
            )
        )

class BusCreateForm(BusForm):
    bus_id = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'readonly':False})
    )


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super(RouteForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('starting_point'),Column('destination')),
            Row(Column('distance'),Column('total_time')),
            FormActions(
                Submit('save','Save',css_class='cus-save-btn'),
                css_class='d-grid gap-2 d-flex justify-content-end'
            )
        )