from django.db import models
from django.core.validators import ValidationError

from datetime import datetime,date,time,timedelta

from employees.models import Driver,BusStaff

MIN_DELTA_TIME_TRIP_SPAN = timedelta(hours=12)


class BusChoices(models.TextChoices):
    NORM = 'NORMAL','Normal'
    LIMO = 'LIMO', 'Limousine'
    VIP  = 'VIP', 'Vip'

class Route(models.Model):
    class Meta:
        managed = False
        db_table = 'route'
    
    route_id = models.AutoField(primary_key=True)
    starting_point = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    distance = models.IntegerField(null=True,blank=True,default=None)
    total_time = models.TimeField()

    def __str__(self):
        return f'{self.starting_point} - {self.destination}'
    

class Stop(models.Model):
    class Meta:
        managed = False
        db_table = 'stop'
    
    stop_id = models.BigAutoField(primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE,
        db_column='route_id',related_name='stops')
    stop_address = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.stop_id:05d}'
    

class TripSchedule(models.Model):
    class Meta:
        managed = False
        db_table = 'trip_schedule'

    class DateChoices(models.TextChoices):
        MONDAY = 'MON','Monday'
        TUESDAY = 'TUE','Tuesday'
        WEDNESDAY = 'WED','Wednesday'
        THURSDAY = 'THU','Thursday'
        FRIDAY = 'FRI','Friday'
        SATURDAY = 'SAT','Saturday'
        SUNDAY = 'SUN','Sunday'

    sched_id = models.AutoField(primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.RESTRICT,
        db_column='route_id',related_name='trip_scheds')
    passenger_price = models.DecimalField(max_digits=10,decimal_places=2)
    luggage_price = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.TextField(max_length=3,choices=DateChoices.choices)
    departure_time = models.TimeField()
    arrival_time = models.TimeField(null=False,blank=True)
    bustype = models.TextField(choices=BusChoices.choices)

    def __str__(self):
        # return f'{self.sched_id:02d}'
        return f'{self.DateChoices(self.date).label}  {self.route}   {self.departure_time} - {self.arrival_time}'

    def save(self,*args, **kwargs):
        ddt = datetime.combine(date.min, self.departure_time) +\
            (datetime.combine(date.min, self.route.total_time) - datetime.min)
        self.arrival_time = ddt.time()
        super(TripSchedule, self).save(*args, **kwargs)


class Bus(models.Model):
    class Meta:
        managed = False
        db_table = 'bus'

    class SleeperTypeChoice(models.TextChoices):
        SINGLE = 'SINGLE','Single'
        DOUBLE = 'DOUBLE', 'Double'
        CABIN  = 'CABIN', 'Cabin'

    bus_id = models.CharField(max_length=10,primary_key=True)
    bustype = models.TextField(choices=BusChoices.choices)
    total_seat = models.IntegerField()
    maxload = models.IntegerField()
    sleeper_type = models.TextField(choices=SleeperTypeChoice.choices)

    def __str__(self):
        return f'{self.bus_id} {self.bustype}'
    

class Trip(models.Model):
    class Meta:
        managed = False
        db_table = 'trip'
    
    trip_id = models.BigAutoField(primary_key=True)
    sched = models.ForeignKey(TripSchedule, on_delete=models.RESTRICT,
        db_column='sched_id',related_name='trips')
    departure_date = models.DateField()
    bus = models.ForeignKey(Bus, on_delete=models.DO_NOTHING,
        db_column='bus_id',related_name='trips')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL,
        db_column='driver_id',related_name='trips',null=True)
    trip_staffs = models.ManyToManyField(BusStaff,through='TripStaff',
        related_name='trips')
    empty_seats = models.IntegerField(blank=True)

    def __str__(self):
        # return f'{self.trip_id:011d}'
        return f'{self.departure_date} {self.sched}'

    def clean(self,*args, **kwargs):
        super(Trip,self).clean(*args, **kwargs)

        departure_sched = datetime.combine(self.departure_date, self.sched.departure_time)
        arrival_sched = datetime.combine(self.departure_date, self.sched.arrival_time)

        # bustype in bus and bustype in trip_schedule
        if self.bus.bustype != self.sched.bustype:
            error = f'bustype must be {self.sched.bustype}'
            raise ValidationError({'bus':error})

        # departure_date and trips_chedule date
        WEEKDAYS = ['MON','TUE','WED','THU','FRI','SAT','SUN']
        if self.sched.date!=WEEKDAYS[self.departure_date.weekday()]:
            error = f'Weekday must be {TripSchedule.DateChoices(self.sched.date).label}'
            raise ValidationError({'departure_date':error})

        # driver
        driver_sched = self.driver.trips.all()
        if self.trip_id is not None:
            driver_sched=driver_sched.exclude(trip_id = self.trip_id)
        for trip in driver_sched:
            departure_dt = datetime.combine(trip.departure_date, trip.sched.departure_time)
            arrival_dt = datetime.combine(trip.departure_date, trip.sched.arrival_time)
            if not (departure_sched-arrival_dt > MIN_DELTA_TIME_TRIP_SPAN \
                or departure_dt-arrival_sched > MIN_DELTA_TIME_TRIP_SPAN):
                raise ValidationError({'driver':'Driver not available'})
    
    def save(self,*args, **kwargs):
        self.full_clean()

        self.update_empty_seats()
        super(Trip, self).save(*args, **kwargs)
        

    def update_empty_seats(self):
        tickets = self.tickets.all()
        seat_ctr = 0
        for t in tickets:
            if t.ticket_type == "passenger ticket":
                seat_ctr += 1
        self.empty_seats = self.bus.total_seat - seat_ctr

    @property
    def is_due(self):
        today = datetime.now()
        return self.departure_date < today.date() or \
            (self.departure_date == today.date() and self.sched.departure_time < today.time())

    @property
    def remain_load(self):
        tickets = self.tickets.all()
        current_load = 0
        for t in tickets:
            if t.ticket_type == "luggage ticket":
                current_load += t.get_child().weight
        return self.bus.maxload - current_load


class TripStaff(models.Model):
    class Meta:
        managed = False
        db_table = 'trip_staff'

    staff_id = models.BigAutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE,
        db_column='trip_id')
    ee = models.ForeignKey(BusStaff, on_delete=models.SET_NULL,
        db_column='ee_id',null=True)