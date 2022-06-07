from django.db import models

from trips.models import Trip
from customers.models import Customer,SalesPromotion

class PaymentMethods(models.Model):
    class Meta:
        managed = False
        db_table = 'payment_methods'
    
    method_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    class Meta:
        managed = False
        db_table = 'ticket'

    ticket_id = models.BigAutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE,
        db_column='trip_id',related_name='tickets')
    start_location = models.CharField(max_length=100)
    paid = models.BooleanField()
    payment_method = models.ForeignKey(PaymentMethods, on_delete=models.SET_NULL,
        db_column='payment_method',null=True,blank=True,default=None)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
        db_column='customer_id',related_name='tickets')
    program = models.ForeignKey(SalesPromotion, on_delete=models.SET_NULL,
        db_column='program_id',null=True,blank=True,default=None)
    total_cost = models.DecimalField(max_digits=10,decimal_places=2,blank=True)

    def __str__(self):
        return f'{self.ticket_id:011d}'

    @property
    def ticket_type(self):
        if hasattr(self, 'pt_child'):
            return "passenger ticket"
        if hasattr(self, 'lt_child'):
            return "luggage ticket"
        return "undefined"

    def get_child(self):
        if self.ticket_type == "passenger ticket":
            return self.pt_child
        if self.ticket_type == "luggage ticket":
            return self.lt_child
        return None

class PassengerTicket(Ticket):
    class Meta:
        managed = False
        db_table = 'passenger_ticket'
    
    pt_id = models.OneToOneField(Ticket, on_delete=models.CASCADE,
        primary_key=True,parent_link=True,db_column='ticket_id',
        related_name='pt_child')
    seat_num = models.IntegerField()

    def __str__(self):
        return f'{self.pt_id} {self.seat_num}'

    
    def save(self,*args, **kwargs):
        print(self.total_cost)
        if self.total_cost is None:
            ticket_price = float(self.trip.sched.passenger_price)
            if self.program is not None:
                self.total_cost = ticket_price*(1-self.program.discount_rate)
            else:
                self.total_cost = ticket_price
        super(PassengerTicket, self).save()

    

class LuggageTicket(Ticket):
    class Meta:
        managed = False
        db_table = 'luggage_ticket'

    lt_id = models.OneToOneField(Ticket, on_delete=models.CASCADE,
        primary_key=True,parent_link=True,db_column='ticket_id',
        related_name='lt_child')
    weight = models.IntegerField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.pt_id} {self.description}'

    def save(self,*args, **kwargs):
        if self.total_cost is None:
            ticket_price = float(self.trip.sched.luggage_price)
            if self.program is not None:
                self.total_cost = ticket_price*(1-self.program.discount_rate)
            else:
                self.total_cost = ticket_price
        super(LuggageTicket, self).save()