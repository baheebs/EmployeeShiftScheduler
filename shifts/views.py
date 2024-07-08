from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import LoginForm, UserRegistrationForm, LocationForm, EmployeeForm, EmployeeShiftForm, ScheduleReportForm
from .models import User, Location, Employee, EmployeeShift
from django.urls import reverse
from django.http import JsonResponse
import json
import datetime
from datetime import datetime, timedelta
import os
import csv
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse

def landing_view(request):
    return render(request, 'landing.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Create the user
            user = User.objects.create_user(email=email, password=password, name=name)
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    error_message = None
    
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))
            else:
                error_message = 'Invalid username or password'
    
    return render(request, 'auth/login.html', {'form': form, 'error_message': error_message})


@login_required
def home_view(request):
    return render(request, 'home.html')


# locations
@login_required
def location_view(request, location_id=None):
    user_id = request.user.id  
    locations = Location.objects.filter(user_id=user_id) 

    form = LocationForm()

    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            new_location = form.save(commit=False)
            new_location.user = request.user
            new_location.save()


            return JsonResponse({'success': True, 'message': 'Location created successfully'})
        else:
            # Form data is invalid, return validation errors
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)  # 400 for bad request

    context = {
        'form': form,
        'locations': locations
    }
    return render(request, 'locations.html', context)


# edit location
@login_required
def update_location(request, id):
    location = get_object_or_404(Location, id=id)
    
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    return redirect('locations')

# delete location
@login_required
def delete_location(request, id):
    location = get_object_or_404(Location, id=id)
    if request.method == 'POST':
        location.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)


# employees
@login_required
def employee_view(request, employee_id=None):
    user_id = request.user.id  
    employees = Employee.objects.filter(user_id=user_id) 

    form = EmployeeForm()

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            new_employee = form.save(commit=False)
            new_employee.user = request.user
            new_employee.save()


            return JsonResponse({'success': True, 'message': 'Employee created successfully'})
        else:
            # Form data is invalid, return validation errors
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)  # 400 for bad request

    context = {
        'form': form,
        'employees': employees
    }
    return render(request, 'employees.html', context)


# edit employee
@login_required
def update_employee(request, id):
    employee = get_object_or_404(Employee, employee_id=id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    return redirect('employees')

# delete employee
@login_required
def delete_employee(request, id):
    employee = get_object_or_404(Employee, employee_id=id)
    if request.method == 'POST':
        employee.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)


def employees_shift_view(request):
    user_id = request.user.id  
    employees = Employee.objects.filter(user_id=user_id) 
    locations = Location.objects.filter(user_id=user_id) 
    employee_shifts = EmployeeShift.objects.filter(employee__user_id=user_id)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            employee_ids = data.get('employee_ids', [])
            location_id = data.get('location', None)
            start_date = data.get('start_date', None)
            end_date = data.get('end_date', None)
            from_time = data.get('from_time', None)
            to_time = data.get('to_time', None)

            if not (location_id and start_date and end_date and from_time and to_time):
                raise ValueError("Missing required fields in the request.")

            location = Location.objects.get(id=location_id)
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            # Adjust time parsing to handle both '%H:%M:%S' and '%H:%M' formats
            try:
                from_time = datetime.strptime(from_time, '%H:%M:%S').time()
            except ValueError:
                from_time = datetime.strptime(from_time, '%H:%M').time()
            try:
                to_time = datetime.strptime(to_time, '%H:%M:%S').time()
            except ValueError:
                to_time = datetime.strptime(to_time, '%H:%M').time()

            for employee_id in employee_ids:
                employee = Employee.objects.get(employee_id=employee_id)
                current_date = start_date
                while current_date <= end_date:
                    # Check if shift already exists for the employee on the same day and time
                    if not EmployeeShift.objects.filter(employee=employee, date=current_date, from_time=from_time, to_time=to_time).exists():
                        EmployeeShift.objects.create(
                            user=request.user,
                            employee=employee,
                            location=location,
                            date=current_date,
                            from_time=from_time,
                            to_time=to_time
                        )
                    current_date += timedelta(days=1)

            return JsonResponse({'status': 'success', 'message': 'Shifts scheduled successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    context = {
        'employees': employees,
        'locations': locations,
        'employee_shifts': employee_shifts,
    }
    
    return render(request, 'employees_shift.html', context)



# delete shift
@login_required
def delete_employees_shift(request, id):
    shift = get_object_or_404(EmployeeShift,id=id)
    if request.method == 'POST':
        shift.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)


# generate schedule report
@login_required
def generate_report(request):
    if request.method == 'POST':
        form = ScheduleReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            email = form.cleaned_data['email']

            shifts = EmployeeShift.objects.filter(date__range=[start_date, end_date])

            # Generate CSV file
            csv_file_name = f"schedule_report_{start_date}_{end_date}.csv"
            csv_file_path = os.path.join(settings.MEDIA_ROOT, csv_file_name)
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Employee ID', 'Employee Name', 'Location', 'Date', 'From Time', 'To Time', 'Department'])
                for shift in shifts:
                    writer.writerow([
                        shift.employee.employee_id,
                        shift.employee.full_name,
                        shift.location.name,
                        shift.date,
                        shift.from_time,
                        shift.to_time,
                        shift.employee.department
                    ])

            email_subject = 'Employee Shift Schedule Report'
            email_body = 'Please find the attached shift schedule report.'
            email_message = EmailMessage(email_subject, email_body, to=[email])
            email_message.attach_file(csv_file_path)
            email_message.send()
            response = HttpResponse(open(csv_file_path, 'rb').read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={csv_file_name}'
            return response
    else:
        form = ScheduleReportForm()

    return render(request, 'report.html', {'form': form})