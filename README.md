# EmployeeShiftScheduler


This project is an Employee Shift Management System built with Django, Celery, and Redis. Below are the steps to set up and run Celery with Django.

## Prerequisites

- Python 3.12
- Redis
- Django
- Celery

Celery run
celery -A shift_management.celery worker --pool=solo -l info
celery -A shift_management beat -l info


## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/employee_shift.git

