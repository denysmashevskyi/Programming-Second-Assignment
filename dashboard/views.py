from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import user_passes_test
from .decorators import allowed_users


from .form import TrainForm
from dashboard import models, form

def admin_required(user):
    return user.groups.filter(name='Admins').exists()

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = TrainForm(request.POST)
        if form:
            # From = form.cleaned_data['From']
            # To = form.cleaned_data['To']
            # trains = Train.objects.filter(route__start=From, route__end=To)
            return redirect('')
    else:
        form = TrainForm()
        return render(request, 'search_flight.html')
    
@login_required
def find_trains(request):
    if request.method == 'POST':
        form = TrainForm(request.POST)
        if form:
            # From = form.cleaned_data['From']
            # To = form.cleaned_data['To']
            # trains = Train.objects.filter(route__start=From, route__end=To)
            return render(request, 'find-trains.html')
        else: return redirect('dashboard')


def context_data():
    context = {
        'page_name' : '',
        'page_title' : '',
        'system_name' : ' Reservation Managament System',
        'topbar' : True,
        'footer' : True,
    }

    return context
@login_required
def search_flight(request):
    context = {
        'page': 'Search Available Flight',
        'airports': models.TrainStop.objects.filter(delete_flag=0).all()
    }
    return render(request, 'search_flight.html', context)

@login_required
def search_results(request):
    from_airport = request.GET.get('from_airport')
    to_airport = request.GET.get('to_airport')
    departure_date = request.GET.get('departure')
    
    if from_airport and to_airport and departure_date:
        departure_date = datetime.datetime.strptime(departure_date, "%Y-%m-%d")
        flights = models.Flights.objects.filter(
            from_airport_id=from_airport,
            to_airport_id=to_airport,
            departure__date=departure_date,
            delete_flag=0
        ).order_by('departure')
        context = {
            'flights': flights,
            'from_airport': from_airport,
            'to_airport': to_airport,
            'departure_date': departure_date
        }
    else:
        messages.error(request, "Please fill in all fields.")
        return redirect('search_flight')
    
    return render(request, 'search_result.html', context)
    
@login_required
@allowed_users(allowed_roles=['admin'])
def list_airport(request):
    context = context_data()
    context['page_title'] ="Airports"
    context['airports'] = models.TrainStop.objects.filter(delete_flag = 0).all()
    return render(request, 'airports.html', context) 

@login_required
@allowed_users(allowed_roles=['admin'])
def manage_airport(request, pk = None):
    if pk is None:
        airport = {}
        print('pk is none')
    else:
        airport = models.TrainStop.objects.get(id = pk)
    context = context_data()
    context['page_title'] ="Manage Airport"
    context['airport'] = airport
    return render(request, 'manage_airport.html', context) 

@login_required
@allowed_users(allowed_roles=['admin'])
def save_airport(request):
    resp = { 'status': 'failed', 'msg':'' }
    if not request.method == 'POST':
       resp['msg'] = "No data has been sent."
    else:
        post = request.POST
        if not post['id'] == '':
            airport = models.TrainStop.objects.get(id = post['id'])
            form1 = form.SaveAirports(request.POST, instance = airport)
        else:
            form1 = form.SaveAirports(request.POST)

        if form.is_valid():
            form.save()
            resp['status'] = 'success'
            if post['id'] == '':
                resp['msg'] = "New Airport has been added successfully."
            else:
                resp['msg'] = "Airport Details has been updated successfully."
            messages.success(request,f"{resp['msg']}")
        else:
            pass
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
@allowed_users(allowed_roles=['admin'])
def delete_airport(request, pk=None):
    resp = { 'status' : 'failed', 'msg' : '' }
    if pk is None:
        resp['msg'] = 'No ID has been sent'
    else:
        try:
            models.TrainStop.objects.filter(id = pk).update(delete_flag = 1)
            resp['status'] = 'success'
            messages.success(request, "Airport has been deleted successfully")
        except:
            resp['msg'] = 'airport has failed to delete'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
@allowed_users(allowed_roles=['admin'])
def list_flight(request):
    context = context_data()
    context['page_title'] ="Flights"
    context['flights'] = models.Flights.objects.filter(delete_flag = 0).all()
    return render(request, 'flights.html', context) 

@login_required
@allowed_users(allowed_roles=['admin'])
def add_flight(request):
    print("method: " , request.method)
    if request.POST:
        form1 = form.NewFlightForm(request.POST) 
        print(request.POST)
        print("method: " , request.method)
        if form1.is_valid():
            form1.save()
            print('Flight added successfully')
            return redirect('flight-page')
        else:
            print(form1.errors)
    
    return render(request, 'add_flight.html', {'form': form.NewFlightForm()})

@login_required
@allowed_users(allowed_roles=['admin'])
def add_train_stop(request):
    if request.POST:
        form1 = form.NewTrainStopForm(request.POST) 
        if form1.is_valid():
            form1.save()
            print('Train Stop added successfully')
            return redirect('airport-page')
        else:
            print(form1.errors)
            
    return render(request, 'add_train_stop.html', {'form': form.NewTrainStopForm()})

@login_required
@allowed_users(allowed_roles=['admin'])
def delete_train_stop(request, pk):
    dele= models.TrainStop.objects.get(id=pk)
    dele.delete()
    return redirect('airport-page')

@login_required
@allowed_users(allowed_roles=['admin'])
def edit_train_stop(request, pk):
    airport = models.TrainStop.objects.get(id=pk)
    if request.method == 'POST':
        form1 = form.NewTrainStopForm(request.POST, instance=airport)
        if form1.is_valid():
            form1.save()
            return redirect('airport-page')
    else:
        form1 = form.NewTrainStopForm(instance=airport)
    return render(request, 'edit_train_stop.html', {'form': form, 'airport': airport})

@login_required
@allowed_users(allowed_roles=['admin'])
def delete_trip(request, pk):
    dele= models.Flights.objects.get(id=pk)
    dele.delete()
    return redirect('flight-page')

@login_required
@allowed_users(allowed_roles=['admin'])
def edit_trip(request, pk):
    flight = models.Flights.objects.get(id=pk)
    if request.method == 'POST':
        form1 = form.NewFlightForm(request.POST, instance=flight)
        if form1.is_valid():
            form1.save()
            return redirect('flight-page')
    else:
        form1 = form.NewFlightForm(instance=flight)
    return render(request, 'edit_trip.html', {'form': form1, 'flight': flight})

@login_required
def home(request):
    context = context_data()
    
    return render(request, 'home.html', context)

# def add_flight(request):
#     if request.method == 'POST':
#         forms = form.FlightForm(request.POST)
#         if forms.is_valid():
#             forms.save()
#             return json.JsonResponse({'message': 'Flight added successfully'})
#         else:
#             print('zupa')
#     else:
#         forms = form.FlightForm()
#         print('zlupa')
#     return render(request, 'add_flight.html', {'form': forms})



@login_required
def list_reservation(request):
    context = context_data()
    context['page_title'] ="Reservations"
    context['reservations'] = models.Reservation.objects.filter(user=request.user).all()
    return render(request, 'reservation_list.html', context) 

@login_required
def reserve_ticket(request, flight_id):
    flight1 = models.Flights.objects.get(id=flight_id)
    if request.method == 'POST':
        form1 = form.ReservationForm(request.POST)
        if form1.is_valid():
            seat_type = form1.cleaned_data['type']
            if seat_type == '1' and flight1.business_class_slots == 0:
                messages.error(request, 'No business class seats available.')
            elif seat_type == '2' and flight1.economy_slots == 0:
                messages.error(request, 'No economy class seats available.')
            else:
                reservation = form1.save(commit=False)
                reservation.flight = flight1
                reservation.user = request.user
                reservation.status = '0'  
                reservation.route_id = flight1.id
                reservation.save()
                if seat_type == '1':
                    flight1.business_class_slots -= 1
                elif seat_type == '2':
                    flight1.economy_slots -= 1
                flight1.save()
                return redirect('reservation')
    else:
        form1 = form.ReservationForm()
    return render(request, 'reservation_form.html', {'form': form1, 'flight': flight1})

@login_required
def reservation_details(request, reservation_id):
    reservation = models.Reservation.objects.get(id=reservation_id)
    return render(request, 'reservation_details.html', {'reservation': reservation})

@login_required
def update_reservation_status(request, reservation_id):
    reservation = models.Reservation.objects.get(id=reservation_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['1', '2']:
            reservation.status = status
            reservation.save()
    return redirect('reservation')

@login_required
def delete_reservation(request, pk):
    dele= models.Reservation.objects.get(id=pk)
    dele.delete()
    return redirect('reservation')


@login_required
def share_trip(request):
    if request.method == 'POST':
        form1 = form.SharedTripForm(request.POST)
        if form1.is_valid():
            shared_trip = form1.save(commit=False)
            shared_trip.user = request.user
            shared_trip.save()
            return redirect('shared_trips')
    else:
        form1 = form.SharedTripForm()
    return render(request, 'share_trip.html', {'form': form1})

@login_required
def shared_trips(request):
    trips = models.SharedTrip.objects.all()
    return render(request, 'shared_trips.html', {'trips': trips})



@login_required
def share_reserved_trip(request, reservation_id):
    reservation = models.Reservation.objects.get(id=reservation_id, user=request.user)
    if request.method == 'POST':
        form1 = form.SharedTripForm(request.POST)
        if form1.is_valid():
            shared_trip = form1.save(commit=False)
            shared_trip.user = request.user
            shared_trip.save()
            return redirect('shared_trips')
    else:
        initial_data = {
            'title': f'Trip from {reservation.route.from_airport.name} to {reservation.route.to_airport.name}',
            'trip_date': reservation.route.departure,
            'from_location': reservation.route.from_airport.name,
            'to_location': reservation.route.to_airport.name,
            'departure': reservation.route.departure,
            'arrival': reservation.route.estimated_arrival,
        }
        form1 = form.SharedTripForm(initial=initial_data)
    return render(request, 'share_reserved_trip.html', {'form': form1, 'reservation': reservation})

def delete_shared_trip(request, pk):
    dele= models.SharedTrip.objects.get(id=pk)
    dele.delete()
    return redirect('shared_trips')