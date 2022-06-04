from django import forms
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Row,Column,Submit,Button
from crispy_forms.bootstrap import InlineRadios,FormActions

from .models import *

class EmployeeForm(forms.ModelForm):
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date'} 
        )
    )

    def __init__(self,*args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    def clean_phone(self):
        data = self.cleaned_data["phone"]
        if len(data) != 10:
            raise forms.ValidationError('Phone number must have 10 digits')
        return data
    
    

class ManagerForm(EmployeeForm):
    class Meta:
        model = Manager
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super(ManagerForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(Column('fname'),Column('lname'),Column('sex')),
            Row(Column('birth_date'),Column('phone')),
            Row(Column('salary'),Column('manager_id'),Column('certificate_id')),
            Row(Column('address')),

            FormActions(
                Submit('save','Save'),
                Button(
                    'back','Back',
                    css_class='btn btn-secondary',
                    onClick = f"javascript:location.href='{reverse_lazy('employees:index')}';"
                )
            )
        )

class DriverForm(EmployeeForm):
    class Meta:
        model = Driver
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(Column('fname'),Column('lname'),Column('sex')),
            Row(Column('birth_date'),Column('phone')),
            Row(Column('salary'),Column('manager_id')),
            Row(Column('license_id'),Column('exp_year')),
            Row(Column('address')),

            FormActions(
                Submit('save','Save'),
                Button(
                    'back','Back',
                    css_class='btn btn-secondary',
                    onClick = f"javascript:location.href='{reverse_lazy('employees:index')}';"
                )
            )
        )


class BusStaffForm(EmployeeForm):
    class Meta:
        model = BusStaff
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super(BusStaffForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(Column('fname'),Column('lname'),Column('sex')),
            Row(Column('birth_date'),Column('phone')),
            Row(Column('salary'),Column('manager_id'),Column('vaccine')),
            Row(Column('address')),

            FormActions(
                Submit('save','Save'),
                Button(
                    'back','Back',
                    css_class='btn btn-secondary',
                    onClick = f"javascript:location.href='{reverse_lazy('employees:index')}';"
                )
            )
        )


class TelephoneStaffForm(EmployeeForm):
    class Meta:
        model = TelephoneStaff
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super(TelephoneStaffForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(Column('fname'),Column('lname'),Column('sex')),
            Row(Column('birth_date'),Column('phone')),
            Row(Column('salary'),Column('manager_id')),
            Row(Column('address')),

            FormActions(
                Submit('save','Save'),
                Button(
                    'back','Back',
                    css_class='btn btn-secondary',
                    onClick = f"javascript:location.href='{reverse_lazy('employees:index')}';"
                )
            )
        )
