from django.db import models
from datetime import datetime

from employees.models import Driver,BusStaff

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
    total_time = models.TimeField(null=True,blank=True,default=None)

    def __str__(self):
        return f'{self.route_id:03d}'
    

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
    arrival_time = models.TimeField(null=True,blank=True,default=None)
    bustype = models.TextField(choices=BusChoices.choices,null=True,
        blank=True,default=None)

    def __str__(self):
        return f'{self.sched_id:02d}'


class Bus(models.Model):
    class Meta:
        managed = False
        db_table = 'bus'

    class SleeperTypeChoice(models.TextChoices):
        SINGLE = 'SINGLE','Single'
        DOUBLE = 'DOUBLE', 'Double'
        CABIN  = 'CABIN', 'Cabin'

    bus_id = models.CharField(max_length=10,primary_key=True)
    bustype = models.TextField(choices=BusChoices.choices,null=True,
        blank=True,default=None)
    total_seat = models.IntegerField()
    maxload = models.IntegerField()
    sleeper_type = models.TextField(choices=SleeperTypeChoice.choices,
        null=True,blank=True,default=None)

    def __str__(self):
        return self.bus_id
    

class Trip(models.Model):
    class Meta:
        managed = False
        db_table = 'trip'
    
    trip_id = models.BigAutoField(primary_key=True)
    sched = models.ForeignKey(TripSchedule, on_delete=models.RESTRICT,
        db_column='sched_id',related_name='trips')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(null=True,blank=True,default=None)
    bus = models.ForeignKey(Bus, on_delete=models.DO_NOTHING,
        db_column='bus_id',related_name='trips')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL,
        db_column='driver_id',related_name='trips',null=True)
    trip_staffs = models.ManyToManyField(BusStaff,through='TripStaff',
        related_name='trips')
    empty_seats = models.IntegerField()

    def __str__(self):
        return f'{self.trip_id:011d}'

    @property
    def is_due(self):
        today = datetime.now()
        return self.departure_time.date() < today.date() or \
            (self.departure_time.date() == today.date() and self.departure_time.time() < today.time())


class TripStaff(models.Model):
    class Meta:
        managed = False
        db_table = 'trip_staff'

    staff_id = models.BigAutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE,
        db_column='trip_id')
    ee = models.ForeignKey(BusStaff, on_delete=models.SET_NULL,
        db_column='ee_id',null=True)