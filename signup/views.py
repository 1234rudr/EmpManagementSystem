from django.conf import settings
from django.shortcuts import render, redirect,HttpResponse
from .models import *
from django.contrib.auth import authenticate,login,logout
import inflect

from datetime import *
from django.db.models import Avg
from django.contrib import messages

from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from django.core.mail import EmailMultiAlternatives


# Create your views here.
def index(request):
    return render(request,"index.html")

# employee login pages>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def emp_login(request):
    if request.method == "POST":
        un = request.POST['email']
        pwd = request.POST['password']
        user =authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            return redirect("employee_home")
            
            
        else:
            messages.success(request,"WORNG CREDENTIALS!!!! PLEASE TRY AGAIN")
            return redirect("employee_login")
            
    return render(request ,"emp_login.html")



#Adding an employee to the list >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>....


def signup(request):
    user = request.user
    employee = employeeDetails.objects.get(user=user)
    hs = Department.objects.all()
    # print("sssssssssssssssssssssssssssss",hs)
    disp={
        'emp':employee,
        'dept':hs
    }
    if request.method == "POST":
        fn= request.POST['first_name']
        ln= request.POST['last_name']
        phone_num= request.POST['phone_num']
        email= request.POST['email']
        password= request.POST['password']
        alt_email=request.POST['alt_email']
        alt_phone=request.POST['alt_phone_num']
        emp_code=request.POST['emp_code']
        adhar_num=request.POST['adhar_num']
        doj=request.POST['doj']
        dob=request.POST['dob']
        full_name=request.POST['full_name']
        name_bank=request.POST['name_bank']
        ifsc=request.POST['ifsc']
        acc_num=request.POST['acc_num']
        dept2= request.POST['dept']
        role = request.POST['role']
       
        try:
            user = User.objects.create_user(first_name=fn,last_name=ln,username=email,password=password)
            dept1 = Department.objects.get(pk=dept2)
            det =employeeDetails.objects.create(phone_num=phone_num,user=user,
                    alternate_email=alt_email,alter_phone=alt_phone,employee_code=emp_code,
                    adhar_no=adhar_num,joining_date=doj,date_of_birth=dob,name_as_per_bank=full_name,
                    name_of_bank=name_bank,ifsc=ifsc,acc_no=acc_num,dept=dept1,designation=role)
            det1= employeeEducation.objects.create(user=user) #additional after creating user .here its storing user details in the education module after the signup(foregin key)
            # det2=attendence.objects.create(user=user)
            det1.save()
            det.save()
            messages.success(request," Registered sucessfully")
            # det2.save()
            return redirect('all_employees')
        except Exception as e:
            print('e', e)
    return render(request,"registration.html",disp)

# Employee Home PAge>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>....


def employee_home(request):
    user= request.user
    employee=employeeDetails.objects.get(user=user)
    disp={
        'dis' : employee
    }
    messages.success(request,"logged in sucessfully")
    if not request.user.is_authenticated:
        return redirect("employee_login")
    
    return render(request,"employee_home.html",disp)

#Employee Attendence >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.......


def attendencetime(request):
    if not request.user.is_authenticated:
        return redirect("employee_login")

    user = request.user

    employeeee= employeeDetails.objects.get(user=user)

    # Get the latest attendance record or create a new one if it doesn't exist
    attendance = attendence.objects.filter(user=user).last()
    if attendance is None or attendance.is_checked_out():
        # Create a new attendance record if the user doesn't have one or is already checked out
        attendance = attendence.objects.create(user=user)

    if request.method == "POST":
        if attendance.is_checked_in():
            attendance.check_out()
            return redirect("employee_home")
        else:
            attendance.check_in()

    disp={
        "attendance": attendance,
        'dis':employeeee  
    }

    return render(request, "employee_home.html", disp)



def employee_profile(request):
    if not request.user.is_authenticated:
        return redirect("employee_login")
    
    user = request.user
    employee = employeeDetails.objects.get(user=user)
    dis = {'disp': employee}
   
    if request.method == "POST":
        phone_num = request.POST['phone_num']
        email = request.POST['email']
        gender = request.POST['gender']

        if 'img' in request.FILES:
            print("i'm here")
            img = request.FILES['img']
            print("image recieved")
            employee.image = img  # Use 'image' here to match the model field name


        employee.phone_num = phone_num
        employee.email = email
        employee.gender = gender

        try:
            employee.save()
            employee.user.save()
            return redirect("show_profilee")
        except Exception as e:
            print("Error saving employee:", e)
    
    return render(request, "emp_profile.html", dis)



def logout_emp(request):
    logout(request)
    return redirect("index")


def education_details(request):
    if not request.user.is_authenticated:
        return redirect("employee_login") 
    user = request.user
    experience = employeeEducation.objects.get(user=user)
    u = employeeDetails.objects.get(user=user)
    disp={
        'dis':experience,
        'u':u
    }
    
    if request.method == "POST":
        ug_clg_name= request.POST['clg_name_ug']
        specification_ug= request.POST['spec_ug']
        yop_ug = request.POST['yop_ug']
        percentage_ug=request.POST['percentage_ug']

        pu_clg_name= request.POST['clg_name_pu']
        specification_pu= request.POST['spec_pu']
        yop_pu = request.POST['yop_pu']
        percentage_pu=request.POST['percentage_pu']

        school_clg_name= request.POST['clg_name_school']
        specification_school= request.POST['spec_school']
        yop_school = request.POST['yop_school']
        percentage_school=request.POST['percentage_school']

        experience.clg_name_ug =  ug_clg_name
        experience.courseug =  specification_ug
        experience.yop_ug =  yop_ug
        experience.percentage_ug =  percentage_ug
        experience.clg_name_pu =  pu_clg_name
        experience.coursepu =  specification_pu
        experience.yop_pu =  yop_pu
        experience.percentage_pu =  percentage_pu
        experience.clg_name_school =  school_clg_name
        experience.courseschool =  specification_school
        experience.yop_scchool =  yop_school
        experience.percentage_school =  percentage_school

        try:
            experience.save()
            return redirect("show_edu_details")
        except:
            return HttpResponse("some error occured")
        
    return render(request,"education.html",disp)

def show_employee_education(request):
    if not request.user.is_authenticated:
        return redirect("employee_login")
    user = request.user 
    employee = employeeEducation.objects.get(user=user)
    u = employeeDetails.objects.get(user=user)
    disp ={
        'dis':employee,
        'u' :u
    }
    if request.method == "POST":
        university1 = request.POST['ug_university']
        ug_name = request.POST['clg_name']
        ug_spe = request.POST['specification']
        ug_per = request.POST['percentage']
        ug_yop = request.POST['yop_ug']
        university2 = request.POST['pu_university']
        pu_name = request.POST['pu_name']
        pu_spe = request.POST['pu_spec']
        pu_per = request.POST['pu_percentage']
        pu_yop = request.POST.get('pu_youp')       
        university3 = request.POST.get('school_university')
        school_name = request.POST['school_name']
        school_spe = request.POST['school_spec']
        school_per = request.POST['school_percentage']
        school_yop = request.POST['school_yop']
        school = request.FILES.get('pdf_school')
        pu = request.FILES.get('pdf_puc')
        ug = request.FILES.get('pdf_ug')
        
        if school and pu and ug:
            employee.ug_pdf=ug
            employee.pu_pdf=pu
            employee.school_pdf=school

        employee.university_ug =university1
        employee.clg_name_ug =ug_name
        employee.courseug =ug_spe
        employee.percentage_ug =ug_per
        employee.yop_ug =ug_yop
        employee.university_pu =university2
        employee.clg_name_pu =pu_name
        employee.coursepu =pu_spe
        employee.percentage_pu =pu_per
        employee.yop_pu =pu_yop
        employee.university_school =university3
        employee.clg_name_school =school_name
        employee.courseschool =school_spe
        employee.percentage_school =school_per
        employee.yop_scchool =school_yop

        employee.save()

    return render(request,'employee_edu_show.html',disp)


def showProfile(request):
    if not request.user.is_authenticated:
        return redirect("employee_login")
    
    user= request.user
    employee=employeeDetails.objects.get(user=user)
    
    # print(employee)
    disp={
        'dis' : employee,
        
    }
    if request.method == "POST":
        phone_num = request.POST['phone']
        email = request.POST['email']
        gender = request.POST['gender']
        address = request.POST['address']
        
        dob = request.POST['dob']
        pan = request.POST['pan']
        adhar = request.POST['adhar']
        alt_email = request.POST['alt_email']
        alt_num = request.POST['alt_num']

        if 'img' in request.FILES:
            img = request.FILES['img']
            print("image recieved")
            employee.image = img  # Use 'image' here to match the model field name

        employee.phone_num = phone_num
        employee.email = email
        employee.gender = gender
        employee.address=address
        
        employee.date_of_birth=dob
        employee.pan_no=pan
        employee.adhar_no=adhar
        employee.alternate_email=alt_email
        employee.alter_phone=alt_num

        try:
            employee.save()
            employee.user.save()
            return redirect("show_profilee")
        except Exception as e:
            print("Error saving employee:", e)
    
    return render(request,"show_profile.html",disp)


def change_password(request):
    error = ""
    if not request.user.is_authenticated:
        return redirect("employee_login")
    
    user = request.user
    u = employeeDetails.objects.get(user=user)
    if request.method=="POST":
        current_password = request.POST['current_pas']
        new_password = request.POST['new_password']
        try:
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                error="no"
                return redirect("employee_login")
            else:
                error = "not"
        except:
                error = "yes"
    
    dicts={
        'disps' : error,
        'u':u
    }

    return render(request,"change_password.html",locals())


# @login_required
def admin_login(request):
    if request.method == "POST":
        un = request.POST['admin_un']
        pwd = request.POST['admin_password']  

        user= authenticate(username=un,password=pwd)

        try:
            if  user.is_staff:#if the user is admin or staf who have givwn the authority
                login(request,user)
                return redirect("admin_homee")
            else:
               pass
        except:
            messages.warning(request,"INCORRECT USER CREDENTIALS!!! TRY AGAIN!!!!")
            return redirect("admin_loginn")

    return render(request,'adminside/admin_login.html')


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    # messages.success(request,"LOGGED IN SUCCESSFULLY")
    user=request.user
    user1 = employeeDetails.objects.get(user=user)
    # user2 = User.objects.get(user=user1)
    if request.method == "POST":
        # fs = request.POST['fs']
        # ls = request.POST['ls']
        designation = request.POST['designation']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        if 'img' in request.FILES:
            print("i'm here")
            img = request.FILES['img']
            print("image recieved")
            user1.image = img

        # user2.first_name = fs
        # user2.last_name =ls
        user1.designation = designation
        user1.address = address
        user1.phone_num=phone
        user1.email = email
        user1.save()
        # user2.save()
    
    # dicts={
    #     'disps' : error
    # }
        
    disp={
        'emp':user,
        'emps':user1,
        
    }
    
    return render(request,"adminside/admin_home.html",disp)


def adminPwdChange(request):
   
    error = ""
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    
    user = request.user
    employee = employeeDetails.objects.get(user=user)
    # print('ssssssssssssssssssssssssss',employee)
    if request.method=="POST":
        current_password = request.POST['admin_current_pas']
        new_password = request.POST['admin_new_password']
        try:
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                error="no"
                return redirect("index")
            else:
                error = "not"
        except:
                error = "yes"
    
    dicts={
        'disps' : error,
        'emp':employee
    }
    return render(request,"adminside/admin_password_change.html",dicts)

def all_employees(request):
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    user = request.user
    employee1 = employeeDetails.objects.get(user=user)
    employee = employeeDetails.objects.all()
    disp={
        'dis':employee,
        'emp' : employee1
    }
    
    return render(request,"adminside/all_employees.html",disp)


def remove_employees(request,pk=0):
    if not request.user.is_authenticated:
        return redirect("employee_login")
    print(pk)
    if pk:
        try:
            remove_employee = employeeDetails.objects.get(pk=pk)
            
            user_data = User.objects.get(pk=remove_employee.user_id)
            
            user_data.delete()
            
        except:
            pass

    return redirect("all_employees")
    # return render(request,"all_employees.html")


def employeeFullDetails(request,pk):
    
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    
    u = request.user
    employee=employeeDetails.objects.get(user=u)
    if pk:
         data = employeeDetails.objects.filter(pk=pk)
         user = employeeDetails.objects.get(pk=pk)
         user1 = employeeEducation.objects.filter(user_id =user.user_id)   
    disp ={
        'users':data, 
        'user1':user1,
        'emp' :employee   
    }
    return render(request,"adminside/a_fulldetails_employee.html",disp)

def educationSh(request):
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    return render(request,"education_details_all.html")

def educationShDE(request,user_id):
   
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    
    if user_id:   
        employee = employeeEducation.objects.filter(user_id=user_id)
       
    disp={
        'emp' : employee
    }
 
    return render(request,"education_details_all.html",disp)


def displayAttendence(request):
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    
    user = request.user
    employee = employeeDetails.objects.get(user=user)
    
    attend = attendence.objects.all()
    disp={
        'time':attend,
        'emp':employee
    }


    return render(request,"adminside/a_employee_attendence.html",disp)





def perticularAttendence(request, user_id):
    ts = 0
    
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    
    user = request.user
    employee1= employeeDetails.objects.get(user=user)
    
    employee = attendence.objects.filter(user_id=user_id)
    
    for record in employee:
        # Skip records with None values for duration
        if record.duration is None:
            continue
        
        # Extract hours, minutes, and seconds
        try:
            hours, minutes, seconds = map(float, record.duration.split(':'))
        except ValueError:
            # Handle cases where duration is not in "HH:MM:SS" format
            continue

        # Calculate the total seconds for the current record
        record_seconds = hours * 3600 + minutes * 60 + seconds

        # Check for negative timedelta
        if record.checkout_time and record.checkin_time and record.checkout_time < record.checkin_time:
            record_seconds = -record_seconds

        # Add the record's duration to the total duration
        ts += record_seconds

    # Convert total_seconds to a timedelta
    total_duration = timedelta(seconds=ts)

    # Create a datetime object with today's date and the time component
    now = datetime.now()
    new_time = now.replace(hour=total_duration.seconds // 3600, minute=(total_duration.seconds // 60) % 60, second=total_duration.seconds % 60)

    # Format new_time as "hh:mm:ss"
    formatted_time = new_time.strftime("%H:%M:%S")
    
    disp = {
        'time': employee,
        'time2': formatted_time,
        'emp':employee1
    }

    return render(request, "adminside/emp_attendence.html", disp)


def displayBankDetails(request,user_id):
    
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    
    if user_id:
        employee= employeeDetails.objects.filter(user_id=user_id)
        disp={
            'emp' : employee
        }
    

    return render(request,"adminside/bank_details.html",disp)



def salaryy(request,user_id):
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    
    user = request.user
    employee = employeeDetails.objects.get(user=user)
    disp={
        'emp':employee
    }
    
    if request.method == "POST":
        ctc = request.POST["basic"]

        monthly = int(ctc)/12

        basic = monthly*0.4
        house_allowance= basic*(40/100)
        user = salary.objects.create(monthly=monthly,user_id=user_id,ctc=ctc,basic=basic,house_rent_allowance=house_allowance)
        user.save()
        return redirect("all_employees")     
    return render(request,"adminside/salary.html",disp)


def editSalary(request,user_id):
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    
    user = salary.objects.filter(user_id=user_id).last()

    u = request.user
    employee = employeeDetails.objects.get(user=u)
   
    


    if request.method == "POST":
        ca = request.POST["ca"]
        ma = request.POST["ma"]
        sb = request.POST["sb"]
        sa = request.POST["sa"]
        g = request.POST["g"]
        # ga = request.POST["ga"]

        professional_tax=200
       
        

        total = round(user.basic + user.house_rent_allowance + int(ca) + int(ma) + int(sb) + int(sa) + int(g))
        esic = total*0.0075
        if total > 24999:
            total1 = total - professional_tax
        elif total<21000:
            total1= total - esic
        else:
            total1= total-0
        
        p = inflect.engine()
        total_in_words = p.number_to_words(total)
        
        
        
        user1=salary.objects.filter(id=user.id).update(conveyance_allowance=ca,medical_allowance=ma,statutory_bonus=sb,special_allowance=sa,gratuity=g,gross_earning=total,in_words=total_in_words,professional_tax=total1,ESIC=esic)
        return redirect("all_employees")   
    disp = {
        'emp':user,
        'emps':employee
    }

        
    return render(request,"adminside/edit_salary.html",disp)


def payslip(request):
    if not request.user.is_authenticated:
        return redirect("employee_login")
    
    user = request.user
    emp=employeeDetails.objects.filter(user=user)

    user1 = salary.objects.filter(user=user).last()
    print(user1)
    disp ={
        'dis' : emp,
        'dis1' :user1
    }
    return render(request,"payslip.html",disp)

def adminpayslip(request,user_id):
    if not request.user.is_authenticated:
        return redirect("employee_login")
    emp = employeeDetails.objects.filter(user_id=user_id)
    user1 = salary.objects.filter(user_id=user_id).last()
    

    disp={
        'dis':emp,
        'dis1':user1
    }
    return render(request,"payslip.html",disp)


# class GeneratePdf(View):
#      def get(self, request, *args, **kwargs):
        
        
        
         
#         # getting the template
#         pdf = html_to_pdf('payslip.html')
         
#          # rendering the template
#         return HttpResponse(pdf, content_type='application/pdf')

def addExperience(request):
    if not request.user.is_authenticated:
        return redirect("employee_login")
    
    user = request.user
    employee= employeeDetails.objects.get(user=user)
    disp={
        'dis':employee
    }
    
    if request.method =="POST":
        job_tittile= request.POST['p_company']
        company=request.POST['j_tittle']
        startdate=request.POST['sd']
        enddate=request.POST['ed']
        e_letter = request.FILES.get('exp')
        payslip = request.FILES.get('pay')
        other = request.FILES.get('other')
        
        if e_letter and payslip and other:
            employee.experience_pdf=e_letter
            employee.payslip_pdf=payslip
            employee.any_other_pdf=other

        employee.job_tittle=job_tittile
        employee.pre_company_name=company
        employee.start_date=startdate
        employee.end_date=enddate
        employee.save()

    # disp={
    #     'dis':employee
    # }

    return render(request,"edit_experience.html",disp)


def pdfConverter(request):
    user = request.user
    emp = employeeDetails.objects.filter(user=user)
    user1 = salary.objects.filter(user=user).last()

    template_path = 'pdf.html'
    context = {'dis': emp, 'dis1': user1}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="payslip.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


def offerletter(request):
    if not request.user.is_authenticated:
        return redirect("employee_login")
    
    user= request.user
    employee= employeeDetails.objects.get(user=user)
    disp={
        'dis':employee
    }

    return render(request,"adminside/offerletter.html",disp)

# *****************************************************************************************************
# Leave Requests>>>>>>>>>>>>>>>>>>>>>>>>>>>

def leaveRequest(request):
    if not request.user.is_authenticated:
        return redirect("employee_login")
    user = request.user
    emp = employeeDetails.objects.get(user=user)
    
    # employee = LeaveRequests.objects.get(user=user)
    
    disp={
        'u':emp
    }
    if request.method=="POST":
        sub = request.POST['sub']
        fd = request.POST['fd']
        td = request.POST['td']
        exp = request.POST['ex']

        obj = LeaveRequests.objects.create(user=user,subject=sub,from_date=fd,to_date=td,explanation=exp,details=emp)
        obj.save()

    return render(request,"leave.html",disp)

def leaveRequestss(request):
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    user= request.user
    employee = employeeDetails.objects.get(user=user)
    req = LeaveRequests.objects.all()
    # if request.method=="POST":
    #     status = request.method['status']
    #     emp = LeaveRequests.objects.get(user_id=user_id)
       
    #     emp.status = status
    #     emp.save()
    disp={
        'u':employee,
        'req':req
    }
    return render(request,"adminside/leave_requests.html",disp)

def leaveRequestssemp(request):
    if not request.user.is_authenticated:
        return redirect("admin_loginn") 
    
    q = LeaveRequests.objects.all()
    disp={
        'req':q
    }
    sub = 'Leave Request Approval'
    if request.method == "POST":
        
        s = request.POST['status']
        n = request.POST['number']
        req = LeaveRequests.objects.filter(details_id=n).last()
        emp = employeeDetails.objects.get(user_id=n)
        req.status = s
        req.save()
#Code for sending mails to the perticular person>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # if s:
        #     to = settings.EMAILS
        to =[emp.email]
        text_content = "your leave request has been"+" "+s
        from_mail = settings.EMAIL_HOST_USER

        msg = EmailMultiAlternatives(sub,text_content,from_mail,to)
        msg.send()

    return render(request,"adminside/leave_requests.html",disp)

def singleLeave(request,user_id):
    if not request.user.is_authenticated:
        return redirect("admin_loginn")
    
    user = request.user
    emp = employeeDetails.objects.get(user=user)
    leave =LeaveRequests.objects.filter(user_id=user_id)
    disp={
        'u':emp,
        'req':leave
    }
    return render(request,"single_leave.html",disp)

def emp_leave(request):
    if not request.user.is_authenticated:
        return redirect("employee_login")
    user =request.user
    emp = LeaveRequests.objects.filter(user=user)
    employee= employeeDetails.objects.get(user=user)

    disp={
        'req':emp,
        'u':employee
    }

    return render(request,"empside.html",disp)
    
















