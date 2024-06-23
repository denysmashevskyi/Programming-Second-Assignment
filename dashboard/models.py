from django.db import models
from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

    

# class Airlines(models.Model):
#     name = models.CharField(max_length=250)
#     status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
#     delete_flag = models.IntegerField(default = 0)
#     date_added = models.DateTimeField(default = timezone.now)
#     date_created = models.DateTimeField(auto_now = True)

#     class Meta:
#         verbose_name_plural = "List of Airlines"

#     def __str__(self):
#         return str(f"{self.name}")



#     def delete(self, *args, **kwargs):
#         super(Airlines, self).delete(*args, **kwargs)
#         storage, path = self.image_path.storage, self.image_path.path
#         storage.delete(path)


class TrainStop(models.Model):
    name = models.CharField(max_length=250)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Train Stops"

    def __str__(self):
        return str(f"{self.name}")
    

class Flights(models.Model):
    code = models.CharField(max_length=250)
    from_airport = models.ForeignKey(TrainStop, on_delete=models.CASCADE, related_name="From_Airport")
    to_airport = models.ForeignKey(TrainStop, on_delete=models.CASCADE, related_name="To_Airport")
    air_craft_code = models.CharField(max_length=250)
    departure = models.DateTimeField()
    estimated_arrival = models.DateTimeField()
    business_class_slots = models.IntegerField(default=0)
    economy_slots = models.IntegerField(default=0)
    business_class_price = models.FloatField(default=0)
    economy_price = models.FloatField(default=0)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Flights"

    def __str__(self):
        return str(f"{self.code} [{self.from_airport.name} - {self.to_airport.name}]")

    def b_slot(self):
        try:
            reservation = Reservation.objects.exclude(status = 2).filter(flight=self, type = 1).count()
            if reservation is None:
                reservation = 0

        except:
            reservation = 0

        return self.business_class_slots - reservation

    def e_slot(self):
        try:
            reservation = Reservation.objects.exclude(status = 2).filter(flight=self, type = 2).count()
            if reservation is None:
                reservation = 0

        except:
            reservation = 0
        return self.economy_slots - reservation
    
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    route = models.ForeignKey(Flights, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=(('1','Business Class'), ('2','Economy')), default = '2')
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=50, choices=(('Male','Male'), ('Female','Female')), default = 'Male')
    email = models.CharField(max_length=250)
    contact = models.CharField(max_length=250)
    address = models.TextField()
    status = models.CharField(max_length=2, choices=(('0','Pending'),('1','Confirmed'), ('2','Cancelled')), default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Reservations"

    def __str__(self):
        return str(f"{self.route.code} - {self.first_name} {self.last_name}")
    
    def name(self):
        return str(f"{self.last_name}, {self.first_name} {self.middle_name}")
    
class SharedTrip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_shared = models.DateTimeField(default=timezone.now)
    trip_date = models.DateTimeField()
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()

    def __str__(self):
        return self.title