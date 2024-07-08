# employee/tasks.py

import csv
import os
from datetime import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from celery import shared_task
from .models import EmployeeShift, DailyShiftReport

@shared_task
def send_daily_shift_report():
    current_date = datetime.now().date()
    shifts = EmployeeShift.objects.filter(date=current_date)
    print(shifts)
    # Generate CSV file
    csv_file_name = f"daily_shift_report_{current_date}.csv"
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
    report_instance = DailyShiftReport(date=current_date)
    report_instance.report_file.save(csv_file_name, open(csv_file_path, 'rb'), save=True)

    email = 'pikna263@gmail.com'  # Replace with the desired email address
    email_subject = 'Daily Employee Shift Report'
    email_body = 'Please find the attached daily shift schedule report.'
    email_message = EmailMessage(email_subject, email_body, to=[email])
    email_message.attach_file(csv_file_path)
    email_message.send()
