from django.db import models

from datetime import datetime

class Customer(models.Model):
    class Meta:
        managed = False
        db_table = 'customer'

    customer_id = models.BigAutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    birth_date = models.DateField(blank=True,null=True,default=None)
    phone = models.CharField(max_length=20,blank=True,null=True,default=None)
    address = models.CharField(max_length=50,blank=True,null=True,default=None)
    email = models.EmailField(max_length=50,blank=True,null=True,default=None)

    def __str__(self):
        return f'{self.customer_id:011d} - {self.fname} {self.lname}'


class MembershipLevel(models.Model):
    class Meta:
        managed = False
        db_table = 'membership_level'
    
    level_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    minimum_point = models.IntegerField()
    maximum_point = models.IntegerField()

    def __str__(self):
        return self.name


class Membership(models.Model):
    class Meta:
        managed = False
        db_table = 'membership'
    
    member_id = models.BigAutoField(primary_key=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE,
        db_column='customer_id',related_name='membership')
    start = models.DateTimeField(blank=True,default=datetime.now())
    end = models.DateTimeField(null=True,blank=True,default=None)
    level = models.ForeignKey(MembershipLevel, on_delete=models.RESTRICT,default=1,db_column='level')
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.member_id:011d} {self.customer_id}'
    

class SalesPromotion(models.Model):
    class Meta:
        managed = False
        db_table = 'sales_promotion'
    
    program_id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=100,null=True,blank=True,default=None)
    discount_rate = models.DecimalField(max_digits=5,decimal_places=2)
    require_level = models.IntegerField(blank=True,default=0)
    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)

    def __str__(self):
        # return f'{self.program_id:09d}'
        return f'{self.description}'