from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
# from django import forms

User = get_user_model()

class RegisterCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

# class TrainForm(forms.Form):
#     From = forms.CharField(label='From', max_length=200)
#     To = forms.CharField(label='To', max_length=200)
#     date = forms.DateField()
#     time = forms.TimeField()
#     capacity = forms.IntegerField(label='Amount of passengers')
#     price = forms.DecimalField(max_digits=5, decimal_places=2)
#     description = forms.CharField(widget=forms.Textarea)