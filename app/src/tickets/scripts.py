# exec(open(r'.\tickets\scripts.py').read())

from tickets.models import *

print('\nPAYMENT METHOD')
for p in PaymentMethods.objects.all()[:3]:
    print(f'{p.method_id} | {p.name}')

print('\nTICKET')
for t in Ticket.objects.all()[:3]:
    print(f'{t.ticket_id} | {t.trip} | {t.start_location} \
| {t.paid} | {t.payment_method} | {t.customer} | {t.program} | {t.total_cost} | {t.ticket_type}')

print('\nPASSENGER TICKET')
for t in PassengerTicket.objects.all()[:3]:
    print(f'{t.ticket_id} | {t.trip} | {t.start_location} \
| {t.paid} | {t.payment_method} | {t.customer} | {t.program} | {t.total_cost} | {t.seat_num}')

print('\nLUGGAGE TICKET')
for t in LuggageTicket.objects.all()[:3]:
    print(f'{t.ticket_id} | {t.trip} | {t.start_location} \
| {t.paid} | {t.payment_method} | {t.customer} | {t.program} | {t.total_cost} | {t.weight} | {t.description}')