from rest_framework import serializers

from trips.models import Trip

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = [
            'trip_id',
            'route_start',
            'route_dest',
            'departure_date',
            'departure_time',
            'arrival_time',
            'url',
            'is_due',
        ]

    route_start = serializers.SerializerMethodField()
    route_dest  = serializers.SerializerMethodField()
    departure_time  = serializers.SerializerMethodField()
    arrival_time  = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='trips:trip_detail_update',
        lookup_field='trip_id',
        lookup_url_kwarg='pk'
    )

    def get_route_start(self,obj):
        return obj.sched.route.starting_point
    
    def get_route_dest(self,obj):
        return obj.sched.route.destination

    def get_departure_time(self,obj):
        return obj.sched.departure_time
    
    def get_arrival_time(self,obj):
        return obj.sched.arrival_time