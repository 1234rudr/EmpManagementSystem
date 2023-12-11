from django.contrib import admin
from signup.models import *
# Register your models here.
admin.site.register(employeeDetails)
admin.site.register(employeeEducation)
admin.site.register(attendence)
admin.site.register(salary)
admin.site.register(LeaveRequests)
admin.site.register(Department)