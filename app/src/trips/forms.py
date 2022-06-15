from django import forms
from django.urls import reverse_lazy

from django.core.validators import ValidationError

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

    total_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'placeholder': 'hh:mm:ss',
            }
        )
    )

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


class TripScheduleForm(forms.ModelForm):
    class Meta:
        model = TripSchedule
        fields = '__all__'

    departure_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'placeholder': 'hh:mm:ss',
            }
        )
    )

    arrival_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={
                'readonly':True,
                'placeholder': 'hh:mm:ss',
            }
        )
    )

    def __init__(self,*args, **kwargs):
        super(TripScheduleForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('route'),Column('date'),Column('bustype')),
            Row(Column('departure_time'),Column('arrival_time')),
            Row(Column('passenger_price'),Column('luggage_price')),
            FormActions(
                Submit('save','Save',css_class='cus-save-btn'),
                css_class='d-grid gap-2 d-flex justify-content-end'
            )
        )


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'

    departure_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type':'date'}
        )
    )

    def clean_trip_staffs(self):
        departure_sched = datetime.combine(self.cleaned_data['departure_date'], self.cleaned_data['sched'].departure_time)
        arrival_sched = datetime.combine(self.cleaned_data['departure_date'], self.cleaned_data['sched'].arrival_time)

        trip_staffs = self.cleaned_data['trip_staffs']
        overlaped_staffs = []
        for tf in trip_staffs:
            tf_sched = tf.trips.all()
            if self.trip_id is not None:
                tf_sched=tf_sched.exclude(trip_id = self.trip_id)
            for trip in tf_sched:
                departure_dt = datetime.combine(trip.departure_date, trip.sched.departure_time)
                arrival_dt = datetime.combine(trip.departure_date, trip.sched.arrival_time)
                if not (departure_sched-arrival_dt > MIN_DELTA_TIME_TRIP_SPAN \
                    or departure_dt-arrival_sched > MIN_DELTA_TIME_TRIP_SPAN):
                    overlaped_staffs.append(f'{tf.fname} {tf.lname}')
                    break
        if len(overlaped_staffs) != 0:
            error = f'{overlaped_staffs} not available'
            raise ValidationError(error)

        return self.cleaned_data['trip_staffs']

    def __init__(self,*args, **kwargs):
        self.trip_id = None
        if kwargs.get('instance'):
            self.trip_id = kwargs.get('instance').trip_id

        super(TripForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('sched'),Column('departure_date')),
            Row(Column('driver',Row(Column('bus'),Column('empty_seats')),)
                ,Column('trip_staffs')),
            
            FormActions(
                Submit('save','Save',css_class='cus-save-btn'),
                css_class='d-grid gap-2 d-flex justify-content-end'
            )
        )
        self.fields['empty_seats'].disabled = True

class TripDetailForm(TripForm):
    def __init__(self,*args, **kwargs):
        super(TripDetailForm,self).__init__(*args, **kwargs)
        self.fields['sched'].disabled = True