# exec(open(r'.\customers\scripts.py').read())
from customers.models import *

print('\nCUSTOMER')
for e in Customer.objects.all()[:3]:
    print(f'{e.customer_id} | {e.fname} | {e.lname} | \
{e.birth_date} | {e.phone} | {e.address} | {e.email}')

print('\nMEMBERSHIP')
for e in Membership.objects.all()[:3]:
    print(f'{e.member_id} | {e.customer} | {e.start} \
| {e.till} | {e.level} | {e.points}')

print('\nMEMBERSHIP LEVEL')
for e in MembershipLevel.objects.all()[:3]:
    print(f'{e.level_id} | {e.name}')

print('\nSALES PROMOTION')
for e in SalesPromotion.objects.all()[:3]:
    print(f'{e.program_id} | {e.description} | {e.discount_rate} | {e.require_level}')