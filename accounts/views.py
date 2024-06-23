from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from .form import RegisterCustomerForm
from .decorators import unauthenticated_user
# from .form import TrainForm
# from .models import Train

User = get_user_model()

def register_customer(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_customer = True
            var.username = var.email
            var.save()
            messages.success(request, 'Account created. Please login.')
            return redirect('login')
        else:
            print(form.errors)
            messages.warning(request, 'Something went wrong. Please check the form.')
            return redirect('register-customer')
    else:
        form = RegisterCustomerForm()
        context = {"form": form}
        return render(request, 'accounts/register_customer.html', context)
    
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('public-page')
        else:
            messages.warning(request, 'Something went wrong. Please check the form.')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Active session endet. Log in again to continue.')    
    return redirect('login')

@login_required
def home(request):
    return render(request, 'accounts/home.html')


# def find_trains(request):
#     if request.method == 'POST':
#         form = TrainForm(request.POST)
#         if form.is_valid():
#             From = form.cleaned_data['From']
#             To = form.cleaned_data['To']
#             trains = Train.objects.filter(route__start=From, route__end=To)
#             return render(request, 'trains.html', {'trains': trains})
#         else: return redirect('dashboard')
# change password
# update profile