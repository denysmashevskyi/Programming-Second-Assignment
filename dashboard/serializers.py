from rest_framework import serializers
from .models import SharedTrip

class SharedTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedTrip
        fields = '__all__'