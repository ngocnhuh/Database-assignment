# exec(open(r'.\employees\scripts.py').read())
from employees.models import *

print('\nEMPLOYEE')
for e in Employee.objects.all()[:3]:
    print(f'{e.ee_id} | {e.fname} | {e.lname} | {e.birth_date} | {e.sex} \
| {e.phone} | {e.address} | {e.salary} | {e.manager_id}')

print('\nMANAGER')
for e in Manager.objects.all()[:3]:
    print(f'{e.ee_id} | {e.fname} | {e.lname} | {e.birth_date} | {e.sex} | \
{e.phone} | {e.address} | {e.salary} | {e.manager_id} | {e.certificate_id}')

print('\nDRIVER')
for e in Driver.objects.all()[:3]:
    print(f'{e.ee_id} | {e.fname} | {e.lname} | {e.birth_date} | {e.sex} | \
{e.phone} | {e.address} | {e.salary} | {e.manager_id} | {e.license_id} | {e.exp_year}')


print('\nBUS STAFF')
for e in BusStaff.objects.all()[:3]:
    print(f'{e.ee_id} | {e.fname} | {e.lname} | {e.birth_date} | {e.sex} | \
{e.phone} | {e.address} | {e.salary} | {e.manager_id} | {e.vaccine}')


print('\nTELEPHONE STAFF')
for e in TelephoneStaff.objects.all()[:3]:
    print(f'{e.ee_id} | {e.fname} | {e.lname} | {e.birth_date} | {e.sex} | \
{e.phone} | {e.address} | {e.salary} | {e.manager_id}')


print('\nTELE SHIFT')
for ts in TeleShift.objects.all()[:3]:
    print(f'{ts.shift_id} | {ts.ee} | {ts.date} | {ts.start} | {ts.till}')