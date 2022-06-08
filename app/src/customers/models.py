from django.db import models

from django.core.validators import ValidationError

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
        return f'{level} {self.customer_id}'

    def save(self,*args, **kwargs):
        levels = MembershipLevel.objects.all()
        for l in levels:
            if l.minimum_point <= self.points <= (l.maximum_point or 2147483647):
                self.level = l
        super(Membership, self).save(*args, **kwargs)
    

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
        return f'{self.description} - {"Active" if self.is_active else "Inactive"}'

    def clean(self,*args, **kwargs):
        super(SalesPromotion,self).clean(*args, **kwargs)

        if not (0 < self.discount_rate < 1):
            raise ValidationError({'discount_rate':'discount_rate must in range (0,1)'})

    def save(self,*args, **kwargs):
        self.full_clean()
        super(SalesPromotion, self).save(*args, **kwargs)

    @property
    def is_active(self):
        now_date = datetime.now().date()
        now_time = datetime.now().time()

        if now_date < self.start.date() or \
        (now_date == self.start.date() and now_time < self.start.time()):
            return False

        if now_date > self.end.date() or \
        (now_date == self.end.date() and now_time > self.end.time()):
            return False
        
        return True