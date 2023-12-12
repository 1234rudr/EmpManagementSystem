from datetime import date, timezone
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta
import pytz

# Create your models here.
class Department(models.Model):
    dept_name = models.CharField(null=True,max_length=100)

    def __str__(self):
        return self.dept_name

class employeeDetails(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    dept = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    phone_num = models.IntegerField()
    email = models.EmailField(null=True,max_length=30)
    
    designation= models.CharField(max_length=30,null=True)
    gender = models.CharField(max_length=10,null=True)
    joining_date=models.DateField(null=True)
    date_of_birth=models.DateField(null=True)
    employee_code = models.CharField(null=True,primary_key=0,max_length=30)
    pan_no = models.CharField(null=True,max_length=30)
    adhar_no = models.CharField(null=True,max_length=30)
    alter_phone = models.IntegerField(default=0)
    alternate_email= models.EmailField(null=True,max_length=30)
    address = models.CharField(null=True,max_length=250)
    name_as_per_bank=models.CharField(null=True,max_length=150)
    name_of_bank=models.CharField(null=True,max_length=150)
    ifsc=models.CharField(null=True,max_length=30)
    acc_no=models.CharField(null=True,max_length=30)
    image = models.ImageField(upload_to="signup/images",default="")
    twiter = models.CharField(max_length=200 , null=True)
    facebook = models.CharField(max_length=200 , null=True)
    instagram = models.CharField(max_length=200,null=True)
    linkedin = models.CharField(max_length=200 , null=True)

    job_tittle = models.CharField(null=True,max_length=150)
    job_type = models.CharField(null=True,max_length=50)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    pre_company_name=models.CharField(null=True,max_length=200)
    payslip_pdf = models.FileField(upload_to="signup/pdfs",default="")
    experience_pdf = models.FileField(upload_to="signup/pdfs",default="")
    any_other_pdf = models.FileField(upload_to="signup/pdfs",default="")



    def __str__(self):
        return self.user.username

class attendence(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    checkin_time= models.DateTimeField(null=True)
    checkout_time=models.DateTimeField(null=True)
    duration = models.CharField(max_length=20, null=True)
    # duration = models.DurationField(null=True)

    def check_in(self):
        self.checkin_time = datetime.now(pytz.utc)
        self.save()

    def check_out(self):
        self.checkout_time = datetime.now(pytz.utc)
        self.calculate_duration()
        self.save()
        

    def is_checked_in(self):
        return self.checkin_time is not None

    def is_checked_out(self):
        return self.checkout_time is not None
    
    def calculate_duration(self):
        if self.checkin_time and self.checkout_time:
            time_difference = self.checkout_time - self.checkin_time
            # Store duration as a human-readable string
            self.duration = str(time_difference)
        else:
            self.duration = None
    


class employeeEducation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    othre_degree= models.CharField(null=True,max_length=100)
    clg_name = models.CharField(null=True,max_length=200)
    specification=models.CharField(null=True,max_length=100)
    percentage=models.CharField(null=True,max_length=30)
    yop =models.DateField(null=True)
    university = models.CharField(null=True,max_length=200)
    other_pdf = models.FileField(upload_to="signup/pdfs",default="")
    

    university_ug = models.CharField(null=True,max_length=200)
    clg_name_ug=models.CharField(max_length=120,null=True)
    percentage_ug=models.CharField(max_length=20,null=True)
    courseug= models.CharField(max_length=100,null=True)
    yop_ug= models.DateField(null=True)
    ug_pdf = models.FileField(upload_to="signup/pdfs",default="")

    university_pu = models.CharField(null=True,max_length=200)
    coursepu=models.CharField(max_length=50,null=True)
    clg_name_pu=models.CharField(max_length=120,null=True)
    percentage_pu=models.CharField(max_length=20,null=True)
    yop_pu= models.DateField(null=True)
    pu_pdf = models.FileField(upload_to="signup/pdfs",default="")

    university_school = models.CharField(null=True,max_length=200)
    courseschool=models.CharField(max_length=100)
    yop_scchool= models.DateField(null=True)
    clg_name_school=models.CharField(max_length=120,null=True)
    percentage_school=models.CharField(max_length=20,null=True)
    school_pdf = models.FileField(upload_to="signup/pdfs",default="")

    def __str__(self):
        return self.user.username
    

# class employeeExperience(models.Model):

class salary(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ctc = models.FloatField(null=True)
    basic =  models.FloatField(null=True)
    house_rent_allowance = models.IntegerField(null=True)
    conveyance_allowance = models.IntegerField(null=True)
    medical_allowance = models.IntegerField(null=True)
    statutory_bonus = models.IntegerField(null=True)
    special_allowance = models.IntegerField(null=True)
    gratuity = models.IntegerField(null=True)
    gross_earning=models.IntegerField(null=True)
    paid_days = models.IntegerField(null=True)
    in_words = models.CharField(null=True,max_length=250)
    monthly = models.IntegerField(null=True)
    professional_tax = models.IntegerField(null=True)
    ESIC= models.IntegerField(null=True)

    def __str__(self):
        return self.user.username
    
class TypesOfLeaves(models.Model):
    names = models.CharField(null=True,max_length=200)

    def __str__(self):
        return self.names

class LeaveRequests(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    details = models.ForeignKey(employeeDetails,on_delete=models.CASCADE,null=True)
    # subject = models.CharField(null=True,max_length=500)
    subject = models.ForeignKey(TypesOfLeaves,on_delete=models.CASCADE,null=True,blank=True)
    from_date = models.DateField(null=True)
    to_date =models.DateField(null=True)
    explanation = models.CharField(null=True,max_length=1500)
    status = models.CharField(null=True,max_length=20)


    def __str__(self):
        return self.user.first_name

