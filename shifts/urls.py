from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),

    path('locations/', views.location_view, name='locations'),
    path('locations/update/<int:id>/', views.update_location, name='update_location'),
    path('locations/delete/<int:id>/', views.delete_location, name='delete_location'),

    path('employees/', views.employee_view, name='employees'),
    path('employees/update/<int:id>/', views.update_employee, name='update_employee'),
    path('employees/delete/<int:id>/', views.delete_employee, name='delete_employee'),

    path('employees_shift/', views.employees_shift_view, name='employees_shift'),
    path('employees_shift/delete/<int:id>/', views.delete_employees_shift, name='delete_employees_shift'),

    path('reports/', views.generate_report, name='generate_report')

]


