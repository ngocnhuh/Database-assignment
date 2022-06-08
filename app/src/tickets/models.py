from django.db import models

from trips.models import Trip
from customers.models import Customer,SalesPromotion
from django.core.validators import ValidationError

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
    
    def delete(self,*args, **kwargs):
        if hasattr(self.customer,'membership'):
            self.customer.membership.points -= 1
            self.customer.membership.save()
        super(Ticket,self).delete(*args, **kwargs)

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

    def clean(self,*args, **kwargs):
        super(PassengerTicket,self).clean(*args, **kwargs)

        if not (0 < self.seat_num <= self.trip.bus.total_seat):
            error = f'seat_num must be in range [1,{self.trip.bus.total_seat}]'
            raise ValidationError(
                {'seat_num':error}
            )

        qs = self.trip.tickets.all()
        if self.ticket_id is not None:
            qs = qs.exclude(ticket_id=self.ticket_id)

        for ticket in qs:
            if ticket.ticket_type == 'passenger ticket' \
            and ticket.get_child().seat_num == self.seat_num:
                raise ValidationError({'seat_num':('This seat has been reserved')})

    
    def save(self,*args, **kwargs):
        self.full_clean()
        if self.total_cost is None:
            ticket_price = float(self.trip.sched.passenger_price)
            self.total_cost = ticket_price

            if hasattr(self.customer,'membership'):
                self.customer.membership.points += 1
                self.customer.membership.save()
                if self.program is not None and self.program.is_active \
                and self.program.require_level <= self.customer.membership.level.level_id:
                    self.total_cost = ticket_price*(1-self.program.discount_rate)

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

    def clean(self,*args, **kwargs):
        super(LuggageTicket,self).clean(*args, **kwargs)

        qs = self.trip.tickets.all()
        if self.ticket_id is not None:
            qs = qs.exclude(ticket_id=self.ticket_id)

        current_load = self.trip.bus.maxload
        for t in qs:
            if t.ticket_type == "luggage ticket":
                current_load -= t.get_child().weight
        if current_load < self.weight:
            error = f'The remain load is only {current_load}'
            raise ValidationError({'weight':error})


    def save(self,*args, **kwargs):
        self.full_clean()
        if self.total_cost is None:
            ticket_price = float(self.trip.sched.luggage_price)
            self.total_cost = ticket_price

            if hasattr(self.customer,'membership'):
                self.customer.membership.points += 1
                self.customer.membership.save()
                if self.program is not None and self.program.is_active \
                and self.program.require_level <= self.customer.membership.level.level_id:
                    self.total_cost = ticket_price*(1-self.program.discount_rate)
                    
        super(LuggageTicket, self).save()