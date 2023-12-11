"""
URL configuration for login project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="index"),
    path('signup/',views.signup,name="signup"),
    path('emp_login/',views.emp_login,name="employee_login"),
    path('employee_home/',views.employee_home,name="employee_home"),
    path('employee_profile/',views.employee_profile , name="profile"),
    path('logout/',views.logout_emp,name="logoutt"),
    path('admin_login/',views.admin_login,name="admin_loginn"),
    path('education',views.education_details,name="education_details"),
    path('education_details',views.show_employee_education,name="show_edu_details"),
    path('showProf',views.showProfile,name="show_profilee"),
    path('password_change',views.change_password,name="change_passwordd"),
    path('admin_home',views.admin_home,name="admin_homee"),
    path('password_change_admin/',views.adminPwdChange,name="admin_password_change"),
    path('all_employees/',views.all_employees,name="all_employees"),
    path('employee/<int:pk>',views.remove_employees,name="employee"),
    path('view_details_employee',views.employeeFullDetails,name="view_details_employee"),
    path('view_details_employee/<int:pk>',views.employeeFullDetails,name="view_details_employee"),
    path('detailed_edu/',views.educationSh,name="detailed_edu"),
    path('detailed_edu/<int:user_id>',views.educationShDE,name="detailed_edu"),
    path('checkIn/',views.attendencetime, name="attendence"),
    # path('checkout/<int:user_id>',views.attendencetimes, name="attendence_out")
    path('display_attendence',views.displayAttendence,name="display_attendence"),
    path('emp_attendence/<int:user_id>',views.perticularAttendence,name="emp_attendence"),
    path('bank_details/<int:user_id>',views.displayBankDetails,name="view_bank_details"),
    path('salary/<int:user_id>',views.salaryy,name = "salary_details"),
    path('edit_salary/<int:user_id>',views.editSalary,name="edit_salary"),
    path('payslip/',views.payslip,name="payslip"),
    path('adminpay/<int:user_id>',views.adminpayslip,name="adminpayslip"),
    # path('pdf/<int:user_id>', GeneratePdf.as_view()),
    path('pdf/',views.pdfConverter,name="pdfconverter"),
    path('edit_experience/',views.addExperience,name="editexperience"),
    path('grnerate_offer/' ,views.offerletter,name="generateoffer"),


    path('leaveReq/',views.leaveRequest,name="leaveRequet"),
    path('a_leave_req/',views.leaveRequestss,name="requests"),
    # path('a_leave_reqss/<int:user_id>',views.leaveRequestssemp,name="requestsemp"),
    path('a_leave_reqss/',views.leaveRequestssemp,name="requestsemp"),
    path('per_leave/<int:user_id>',views.singleLeave,name="single_leavee"),
    path('emp_leave',views.emp_leave,name="empleave")
    
    
    


]
