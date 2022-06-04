from django.db import models

class Employee(models.Model):
    class Meta:
        managed = False
        db_table = 'employee'
        ordering = ['ee_id']

    class SexChoices(models.TextChoices):
        MALE   = 'M','Male'
        FEMALE = 'F','Female'

    ee_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    birth_date = models.DateField(blank=True,null=True,default=None)
    sex = models.CharField(max_length=4,choices=SexChoices.choices,blank=True,
        null=True,default=None)
    phone = models.CharField(max_length=20,blank=True,null=True,default=None)
    address = models.CharField(max_length=50,blank=True,null=True,default=None)
    salary = models.DecimalField(max_digits=10,decimal_places=2,blank=True,
        null=True,default=None)
    manager_id = models.ForeignKey('employees.Manager', on_delete=models.SET_NULL,
        related_name='employess',blank=True,null=True,default=None,db_column='manager_id')

    def __str__(self):
        return f'{self.ee_id:05d} - {self.fname} {self.lname}'

    @property
    def job_type(self):
        if(hasattr(self, 'mn_child')):
            return 'manager'
        if(hasattr(self, 'dv_child')):
            return 'driver'
        if(hasattr(self, 'bs_child')):
            return 'bus staff'
        if(hasattr(self, 'ts_child')):
            return 'telephone staff'
        return 'undefined'
    
    def get_child(self):
        if self.job_type == 'manager':
            return self.mn_child
        if self.job_type == 'driver':
            return self.dv_child
        if self.job_type == 'bus staff':
            return self.bs_child
        elif self.job_type == 'telephone staff':
            return self.ts_child
        return self


class Manager(Employee):
    class Meta:
        managed = False
        db_table = 'manager'
    mn_id = models.OneToOneField(Employee, on_delete=models.CASCADE, 
        primary_key=True, db_column="ee_id", parent_link=True,
        related_name='mn_child')
    certificate_id = models.CharField(max_length=20,blank=True,null=True,default=None)


class Driver(Employee):
    class Meta:
        managed = False
        db_table = 'driver'
    dv_id = models.OneToOneField(Employee, on_delete=models.CASCADE, 
        primary_key=True, db_column="ee_id", parent_link=True,
        related_name='dv_child')
    license_id = models.CharField(max_length=20)
    exp_year = models.IntegerField()


class BusStaff(Employee):
    class Meta:
        managed = False
        db_table = 'bus_staff'
    bs_id = models.OneToOneField(Employee, on_delete=models.CASCADE, 
        primary_key=True, db_column="ee_id", parent_link=True,
        related_name='bs_child')
    vaccine = models.IntegerField()


class TelephoneStaff(Employee):
    class Meta:
        managed = False
        db_table = 'telephone_staff'
    ts_id = models.OneToOneField(Employee, on_delete=models.CASCADE, 
        primary_key=True, db_column="ee_id", parent_link=True,
        related_name='ts_child')


class TeleShift(models.Model):
    class Meta:
        managed = False
        db_table = 'tele_shift'
        unique_together = (('ee_id','date','start','till'),)

    class DateChoices(models.TextChoices):
        MONDAY    = 'MON','Monday'
        TUESDAY   = 'TUE','Tuesday'
        WEDNESDAY = 'WED','Wednesday'
        THURSDAY  = 'THU','Thursday'
        FRIDAY    = 'FRI','Friday'
        SATURDAY  = 'SAT','Saturday'
        SUNDAY    = 'SUN','Sunday'

    shift_id = models.BigAutoField(primary_key=True)
    ee = models.ForeignKey('employees.TelephoneStaff',
        on_delete=models.CASCADE,db_column='ee_id',unique=False)
    date = models.TextField(max_length=3,choices=DateChoices.choices)
    start = models.TimeField()
    till = models.TimeField()