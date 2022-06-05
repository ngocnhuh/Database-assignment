from django import forms
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Row,Column,Submit,Button
from crispy_forms.bootstrap import InlineRadios,FormActions

from datetime import datetime

from .models import * 

import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date'} 
        )
    )

    def __init__(self,*args, **kwargs):
        super(CustomerForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('fname'),Column('lname'),Column('email')),
            Row(Column('birth_date'),Column('phone')),
            Row(Column('address')),
            FormActions(
                Submit('save','Save',css_class='cus-save-btn'),
                css_class='d-grid gap-2 d-flex justify-content-end'
            )
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError('Invalid email format')
        return email


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['start','end','level','points']

    start = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'placeholder': 'yyyy:mm:dd hh:mm:ss'}),
    )

    end = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'placeholder': 'yyyy:mm:dd hh:mm:ss'}),
    )

    def __init__(self,*args, **kwargs):
        super(MembershipForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('start'),Column('end')),
            Row(Column('level'),Column('points')),
            FormActions(
                Submit('save','Save',css_class='ms-save-btn'),
                css_class='d-grid gap-2 d-flex justify-content-end'
            )
        )