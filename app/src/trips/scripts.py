# exec(open(r'.\trips\scripts.py').read())
from trips.models import *

print('\nROUTE')
for r in Route.objects.all()[:3]:
    print(f'{r.route_id} | {r.starting_point} | {r.destination} \
| {r.distance} | {r.total_time}')

print('\nSTOP')
for s in Stop.objects.all()[:3]:
    print(f'{s.stop_id} | {s.route} | {s.stop_address}')

print('\nTRIP SCHEDULE')
for t in TripSchedule.objects.all()[:3]:
    print(f'{t.sched_id:02d} | {t.route} | {t.passenger_price} | \
{t.luggage_price} | {t.date} | {t.departure_time} | {t.arrival_time} | {t.bustype}')

print('\nBUS')
for b in Bus.objects.all()[:3]:
    print(f'{b.bus_id} | {b.bustype} | {b.total_seat} | {b.maxload} | {b.sleeper_type}')

print('\nTRIP')
for t in Trip.objects.all()[:3]:
    print(f'{t.trip_id} | {t.sched} | {t.departure_date} | \
{t.bus} | {t.driver} | {t.empty_seats}')

