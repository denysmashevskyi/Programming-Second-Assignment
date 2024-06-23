from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from dashboard import models

class TrainForm(forms.Form):
    From = forms.CharField(label='From', max_length=200)
    To = forms.CharField(label='To', max_length=200)
    date = forms.DateField()
    time = forms.TimeField()
    capacity = forms.IntegerField(label='Amount of passengers')
    price = forms.DecimalField(max_digits=5, decimal_places=2)
    description = forms.CharField(widget=forms.Textarea)


class SaveAirports(forms.ModelForm):
    name = forms.CharField(max_length=250)
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.TrainStop
        fields = ('name','status', )

    def clean_name(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            if id > 0:
                airport = models.TrainStop.objects.exclude(id = id).get(name = name, delete_flag = 0)
            else:
                airport = models.TrainStop.objects.get(name = name, delete_flag = 0)
        except:
            return name
        raise forms.ValidationError("Airport is already exists")
    

class NewFlightForm(forms.ModelForm):
    code = forms.CharField(max_length=250)
    air_craft_code = forms.CharField(max_length=250)
    departure = forms.DateTimeField()
    estimated_arrival = forms.DateTimeField()
    from_airport = forms.ModelChoiceField(queryset=models.TrainStop.objects.filter(delete_flag = 0).all())
    to_airport = forms.ModelChoiceField(queryset=models.TrainStop.objects.filter(delete_flag = 0).all())
    business_class_slots = forms.IntegerField()
    economy_slots = forms.IntegerField()
    business_class_price = forms.FloatField()
    economy_price = forms.FloatField()
    class Meta:
        model = models.Flights
        fields = ['air_craft_code', 'departure', 'estimated_arrival', 'from_airport', 'to_airport', 'business_class_slots', 'economy_slots', 'business_class_price', 'economy_price']

class NewTrainStopForm(forms.ModelForm):
    name = forms.CharField(max_length=250)
    class Meta:
        model = models.TrainStop
        fields = ['name']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = models.Reservation
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'email', 'contact', 'address', 'type']

class SharedTripForm(forms.ModelForm):
    class Meta:
        model = models.SharedTrip
        fields = ['title', 'description', 'trip_date', 'from_location', 'to_location', 'departure', 'arrival']
        widgets = {
            'trip_date': forms.HiddenInput(),
            'from_location': forms.HiddenInput(),
            'to_location': forms.HiddenInput(),
            'departure': forms.HiddenInput(),
            'arrival': forms.HiddenInput(),
        }