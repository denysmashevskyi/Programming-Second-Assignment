# from django.shortcuts import render, redirect
# from .form import TrainForm
# from .models import Train

    

# def find_trains(request):
#     if request.method == 'POST':
#         form = TrainForm(request.POST)
#         if form.is_valid():
#             From = form.cleaned_data['From']
#             To = form.cleaned_data['To']
#             trains = Train.objects.filter(route__start=From, route__end=To)
#             return render(request, 'find-trains.html', {'trains': trains})
#         else: return redirect('dashboard')