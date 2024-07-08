from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Location, Employee, EmployeeShift

class UserRegistrationForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    c_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        c_password = cleaned_data.get('c_password')
        if password != c_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = [ 'name']

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = [ 'full_name', 'department', 'date_of_birth']

class EmployeeShiftForm(forms.ModelForm):
    class Meta:
        model = EmployeeShift
        fields = ['employee', 'location', 'date', 'from_time', 'to_time']

class ScheduleReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField()