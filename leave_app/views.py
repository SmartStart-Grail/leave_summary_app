from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views.generic import TemplateView
from django.views import View
from openpyxl import load_workbook
# from leave_app.models import *
from . models import (country_metadata,holiday_metadata,department_metadata,employee_metadata,indirectsupervisor_metadata,
                                             supervisor_metadata,leave_metadata,uploadleave_metadata,project_detail_model,
                                             project_detail,department_head_model,email_model)

from django.contrib.auth.models import User
from django_pandas.io import read_frame
import pandas as pd

from datetime import timedelta
import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin
import calendar

'''Password Reset Import the models'''
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash,authenticate, get_user_model, password_validation,logout
from django.contrib.auth import authenticate, login

from django.contrib import messages
import os
from django.db.models import Q
from ics import Calendar, Event
import platform

from django.utils import timezone
from django.template.loader import render_to_string

'''Email Model Import'''
from utility.email import Mailer
# Create your views here.


def base_view(request):

    return render(request,'base.html')


def login(request):
    return render(request,'login.html')

def test(request):
    return render(request,'testing.html')

'''This functionality used to filter out who is currently login indirect supervisor or direct supervisor'''
def indirect_supervisor(request):
    try:
        indirectsupervisor_metadata.objects.select_related('employee').filter(employee__user_id = request.user.id)
        indirect = indirectsupervisor_metadata.objects.select_related('employee').filter(employee__user_id = request.user.id)
        super = supervisor_metadata.objects.select_related('indirect_supervisor_metadata').filter(indirect_supervisor_metadata_id = indirect[0].id)
        super_emp = supervisor_metadata.objects.select_related('supervisor').filter(supervisor_id__in = list({i.supervisor.id for i in super}))

        indirect_supervisor_obj = supervisor_metadata.objects.select_related('supervisor').filter(supervisor__user_id = request.user.id)
        emp_list = list({i.employee_data.id for i in super_emp})
        if len(indirect_supervisor_obj)>0:
            emp_list = emp_list+list({i.employee_data.id for i in indirect_supervisor_obj})
        return emp_list

    except Exception as e:
            super_emp = supervisor_metadata.objects.select_related('supervisor').filter(supervisor__user_id = request.user.id)
            emp_list = list({i.employee_data.id for i in super_emp})

            return emp_list


def calender_view(request):
    context={
        'title_name':'Calendar','time_off':True
    }

    return render(request,'calendar.html',context)

2
def calendar_function(request,*args,**kwargs):

    background_color = '#3788d8'
    text_color = 'white !important'
    font_size = '5px !important'
    
    if  request.user.id in [1,2]:
        leave_data = leave_metadata.objects.select_related().all()
        holiday_data = holiday_metadata.objects.select_related().all()
        planned = []
        background_color = '#3788d8'
        text_color = 'white !important'
        font_size = '5px !important'
        if len(leave_data)>0:
            for data in leave_data:
                planned.append({
                    'title' :f'{data.employee.first_name} {data.employee.last_name}/ {data.hours}hrs',
                    'id':data.start_date.date(),
                    'hr_off':f'{data.hours}hrs',
                    'start':data.start_date,
                    'end':data.end_date,
                    'backgroundColor':background_color,
                    'textColor':text_color,
                    'fontSize':font_size,
                
                })
        if len(holiday_data)>0:
            for holi in holiday_data:

                city = ''
                if holi.country.name != 'USA':
                    if holi.country.city:
                        city = holi.country.city

                planned.append({
                    'title' :f'{holi.holiday_name}/{holi.country.name} {city}',
                    'id':1,
                    # 'hr_off':f'16hrs',
                    'start':holi.start_date,
                    'end':holi.end_date,
                    'backgroundColor':'rgb(237,125,49)',
                    'textColor':text_color,
                    'fontSize':font_size,
                
                })

        # print(planned)
        return JsonResponse(planned,safe=False)

    elif request.user.id in [-22]:
        user_get = User.objects.get(id = request.user.id)

        work_locations_id = list(
            employee_metadata.objects.filter(user_id = request.user.id)
            .values_list('work_location__name', flat=True)
                )
        
        leave_data = leave_metadata.objects.select_related().filter(employee__work_location__name__in = work_locations_id ,request_status=True)
        holiday_data = holiday_metadata.objects.select_related('country').filter(country__name__in = work_locations_id)
        planned = []
        if len(leave_data)>0:
            for data in leave_data:
                planned.append({
                    'title' :f'{data.employee.first_name} {data.employee.last_name}/ {data.hours}hrs',
                    'id':data.start_date.date(),
                    'hr_off':f'{data.hours}hrs',
                    'start':data.start_date,
                    'end':data.end_date,
                    'backgroundColor':'#3788d8',
                    'textColor':'white !important',
                    'fontSize':font_size,
                
                })
        if len(holiday_data)>0:
            for holi in holiday_data:

                city = ''
                if holi.country.name != 'USA':
                    if holi.country.city:
                        city = holi.country.city

                planned.append({
                    'title' :f'{holi.holiday_name}/{holi.country.name} {city}',
                    'id':1,
                    # 'hr_off':f'16hrs',
                    'start':holi.start_date,
                    'end':holi.end_date,
                    'backgroundColor':'rgb(237,125,49)',
                    'textColor':text_color,
                    'fontSize':font_size,
                
                })

        # print(planned)
        return JsonResponse(planned,safe=False)
    
    else:
        emp_list = indirect_supervisor(request)

        'Below the previous code'
        # user_get = User.objects.get(id = request.user.id)

        work_locations_id = list(
            employee_metadata.objects.filter(user_id = request.user.id)
            .values_list('work_location__name', flat=True)
                )
        
        emp_data_obj = employee_metadata.objects.select_related().filter(id__in = emp_list)

        # Extract employee IDs
        emp_data_id = list(emp_data_obj.values_list('id', flat=True))

        # Optimized country_value extraction (Fixing the loop order issue)
        country_value = list({work_location.name for emp in emp_data_obj for work_location in emp.work_location.all()})

        # Get all holiday data as timezone-aware datetimes
        # holidays = holiday_metadata.objects.select_related('country').filter(
        #     start_date__lte=period_leave, 
        #     end_date__gte=start_date,
        #     country__name__in = country_value
        # )
        leave_data = leave_metadata.objects.select_related().filter(employee__id__in = emp_list ,request_status=True)
        holiday_data = holiday_metadata.objects.select_related('country').filter(country__name__in = country_value)
        planned = []
        if len(leave_data)>0:
            for data in leave_data:
                planned.append({
                    'title' :f'{data.employee.first_name} {data.employee.last_name}/ {data.hours}hrs',
                    'id':data.start_date.date(),
                    'hr_off':f'{data.hours}hrs',
                    'start':data.start_date,
                    'end':data.end_date,
                    'backgroundColor':'#3788d8',
                    'textColor':'white !important',
                    'fontSize':font_size,
                
                })
        if len(holiday_data)>0:
            for holi in holiday_data:

                city = ''
                if holi.country.name != 'USA':
                    if holi.country.city:
                        city = holi.country.city

                planned.append({
                    'title' :f'{holi.holiday_name}/{holi.country.name} {city}',
                    'id':1,
                    # 'hr_off':f'16hrs',
                    'start':holi.start_date,
                    'end':holi.end_date,
                    'backgroundColor':'rgb(237,125,49)',
                    'textColor':text_color,
                    'fontSize':font_size,
                
                })

        # print(planned)
        return JsonResponse(planned,safe=False)

class calendar_view(LoginRequiredMixin,TemplateView):
    template_name = 'calendar.html'

    def get(self,request,*args,**kwargs):

        # if not self.request.user.id in [00]:
        if self.request.user.id in [1,2]:
            emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
            full_name = f'{emp_datas.first_name} {emp_datas.last_name}'
            emp_data = employee_metadata.objects.select_related().all().exclude(id__in=[579]).order_by('first_name')
            emp_data_title = employee_metadata.objects.select_related().all().order_by('job_title')
            emp_supervisor = supervisor_metadata.objects.select_related().all().order_by('supervisor__first_name')
            super_id = []
            super_selected = []
            for emp_datas in emp_supervisor:
                if emp_datas.supervisor.id not in super_id:
                    super_id.append(emp_datas.supervisor.id)
                    super_selected.append(emp_datas)
            dept_data = department_metadata.objects.select_related().all().order_by('dept_name')
            work_id = []
            work_location = []
            work_location_data = country_metadata.objects.select_related().exclude(id=9).order_by('name')
            for work in work_location_data:
                if work.name not in work_id:
                    work_id.append(work.name)
                    work_location.append(work)


            project_data = project_detail_model.objects.select_related().all().order_by('project_name')
            job_title = list({value.job_title  for value in emp_data_title if value.job_title is not None})


            context = {
                'title_name':'Calendar','time_off':True,'emp_data':emp_data,
                'emp_supervisor':super_selected,'dept_data':dept_data,
                'work_location':work_location,'project_data':project_data,
                'job_title':sorted(job_title),
                'full_name':full_name
            }

            return render(request,self.template_name,context)
        

            '''Previous else functionality..'''
        elif request.user.id in [-22]:
            user_get = User.objects.get(id=request.user.id)
        
            # Get department ids for the user
            dept_id = [emp.dept.id for emp in employee_metadata.objects.filter(user=user_get)]
            
            # Get employees in the same department(s)
            emp_dept = employee_metadata.objects.select_related().filter(dept_id__in=dept_id)
            emp_dept_id = [e.id for e in emp_dept]
            # total_emp_count = emp_dept.count()
            emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
            full_name = f'{emp_datas.first_name} {emp_datas.last_name}'
            emp_data = emp_dept
            emp_data_title = emp_dept.order_by('job_title')
            emp_supervisor = supervisor_metadata.objects.select_related().filter(employee_data_id__in = emp_dept_id).order_by('supervisor__first_name')
            super_id = []
            super_selected = []
            for emp_datas in emp_supervisor:
                if emp_datas.supervisor.id not in super_id:
                    super_id.append(emp_datas.supervisor.id)
                    super_selected.append(emp_datas)
            dept_data = department_metadata.objects.select_related().filter(id__in = [e.dept.id for e in emp_dept]).all().order_by('dept_name')
            work_id = []
            work_location = []
            work_location_data = country_metadata.objects.select_related().filter(id__in = [e.work_location.id for e in emp_dept]).exclude(id=9).order_by('name')
            for work in work_location_data:
                if work.name not in work_id:
                    work_id.append(work.name)
                    work_location.append(work)


            '''Project Detail Logic Need to implements'''
            project_data = [
                                data.project_name for data in project_detail.objects
                                .select_related('project_name')  # Pre-fetch related 'project_name'
                                .filter(employee_id__in=emp_dept)  # Filter based on emp_dept list
                                .order_by('project_name__project_name')  # Order by the 'name' field of the related project model
                            ]
            project_data = list(dict.fromkeys(project_data))
            job_title = list({value.job_title  for value in emp_data_title if value.job_title is not None})

            context = {
                'title_name':'Calendar','time_off':True,'emp_data':emp_data,
                'emp_supervisor':super_selected,'dept_data':dept_data,
                'work_location':work_location,'project_data':project_data,
                'job_title':sorted(job_title),
                'full_name':full_name
            }

            return render(request,self.template_name,context)
    
        else:
            emp_data_obj = indirect_supervisor(request)

            emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
            full_name = f'{emp_datas.first_name} {emp_datas.last_name}'
            emp_data = employee_metadata.objects.select_related().filter(id__in = emp_data_obj).exclude(
                                    Q(work_location=None) & Q(user_id__in=[522])
                                    
                                ).order_by('first_name')
            emp_data_title = employee_metadata.objects.select_related().filter(id__in = emp_data_obj).exclude(
                                    Q(work_location=None) & Q(user_id__in=[522])
                                    
                                ).order_by('first_name').order_by('job_title')
            emp_supervisor = supervisor_metadata.objects.select_related('supervisor').filter(employee_data_id__in = emp_data_obj).order_by('supervisor__first_name')
            super_id = []
            super_selected = []
            for emp_datas in emp_supervisor:
                if emp_datas.supervisor.id not in super_id:
                    super_id.append(emp_datas.supervisor.id)
                    super_selected.append(emp_datas)
            # dept_data = department_metadata.objects.select_related().all().order_by('dept_name')

            dept_data = department_metadata.objects.select_related().filter(id__in = [e.dept.id for e in emp_data]).order_by('dept_name')
            work_id = []
            work_location = []  



            #work_location_data = country_metadata.objects.select_related().exclude(id=9).order_by('name')

            work_locations_id = list(
                            employee_metadata.objects.filter(id__in=emp_data_obj)
                            .values_list('work_location__name', flat=True)


                                )
            

            work_location_data = country_metadata.objects.select_related().filter(name__in = work_locations_id).exclude(id=9).order_by('name')
            for work in work_location_data:
                if work.name not in work_id:
                    work_id.append(work.name)
                    work_location.append(work)


            project_data = project_detail_model.objects.select_related().all().order_by('project_name')
            job_title = list({value.job_title  for value in emp_data_title if value.job_title is not None})


            context = {
                'title_name':'Calendar','time_off':True,'emp_data':emp_data,
                'emp_supervisor':super_selected,'dept_data':dept_data,
                'work_location':work_location,'project_data':project_data,
                'job_title':sorted(job_title),
                'full_name':full_name
            }

            return render(request,self.template_name,context)

def new_calender_view(request):
    context={
        'time_off':True
    }

    return render(request,'newcalendar.html',context)


def profile_view(request):
    context = {'title_name':'Profile','setting':True}


    return render(request,'profile.html',context)


# def fiel_upload_view(request):
#     context = { 'title_name':'Upload File','file_upload':True}

#     return render(request,'file_upload.html',context)



'''This Functionality used to import the excel file and then read it store in the database'''
class file_upload_view(LoginRequiredMixin,TemplateView):
    template_name = 'file_upload.html'

    def get(self,request):
        if request.user.id == 1:
            context = {}

            file_data = uploadleave_metadata.objects.all().order_by('-upload_date')[:5]
            project_detail_data = project_detail_model.objects.select_related().all()
            emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
            full_name = f'{emp_datas.first_name} {emp_datas.last_name}'

            context = {'file_data':file_data,'title_name':'Upload File','file_upload':True,'project_detail_data':project_detail_data,
                    'full_name':full_name,
                    }
            return render(request,self.template_name,context)
        else:
            return redirect('home-page')

    def post(self,request):
        excel_file =self.request.FILES['file_upload']
        upload_filed = uploadleave_metadata.objects.create(excel_file = excel_file)
        # df = pd.read_excel(excel_file, header=0, skiprows=7)
        df = pd.read_excel(excel_file,header=None)

        '''In this we read from dataframe and this we filter on basis of first name and remove unwanted row, created the new dataframe'''
        header_row_index = df.apply(lambda row: row.astype(str).str.contains('First Name').any(), axis=1).idxmax()
        # print(df.iloc[header_row_index])
        df.columns = df.iloc[header_row_index]
        df = df.drop(range(header_row_index + 1))
        df.reset_index(drop=True, inplace=True)
        # print(df)

        for index, row in df.iterrows():
            '''Loop over dataframe and save in database'''
            # employee = employee_metadata.objects.filter(first_name= row['First Name'] , last_name = row['Last Name'])
            employee = employee_metadata.objects.filter(employee_id=row['Web Pay ID'])
            if len(employee)>0:
                leave_data = leave_metadata.objects.filter(employee=employee[0],start_date=row['Start Date'],end_date=row['End Date'])
                if len(leave_data)>0:
                    leave_data[0].request_status = True if row['Request Status'] == 'Approved' else False
                    leave_data[0].save()
                    if int(float(row['Hours'])) > 80 and leave_data[0].request_status:

                        try:
                            email_model.objects.get(leave_employee = leave_data)

                        except Exception  as e:
                            # if employee[0].dept and department_metadata.objects.select_related().filter(id = employee[0].dept.id).exists():
                            #     dept_obj = department_metadata.objects.select_related().filter(id = employee[0].dept.id)
                            #     department_head_obj = department_head_model.objects.prefetch_related('department').filter(department = dept_obj[0])
                            #     email_model.objects.create(leave_employee = leave_data[0],department_head = department_head_obj[0],email_send_to = [department_head_obj[0].user.email])
                            super_emp_data = supervisor_metadata.objects.filter(employee_data_id = employee[0].id)
                            if super_emp_data[0].indirect_supervisor_metadata and super_emp_data[0].supervisor:
                                email_send_to  = [super_emp_data[0].indirect_supervisor_metadata.employee.work_email,super_emp_data[0].supervisor.work_email]
                                email_model.objects.create(leave_employee = leave_data[0],email_send_to = email_send_to)

                            elif super_emp_data[0].indirect_supervisor_metadata:
                                email_send_to  = [super_emp_data[0].indirect_supervisor_metadata.employee.work_email]
                                email_model.objects.create(leave_employee = leave_data[0],email_send_to = email_send_to)

                            elif super_emp_data[0].supervisor:
                                email_send_to  = [super_emp_data[0].supervisor.work_email]
                                email_model.objects.create(leave_employee = leave_data[0],email_send_to = email_send_to)

                            else:
                                pass



                else:
                    leave_meta_obj = leave_metadata.objects.create(employee=employee[0],start_date=row['Start Date'],end_date=row['End Date'],
                                                hours=int(float(row['Hours'])),request_status =True if row['Request Status'] == 'Approved' else False,
                                                upload_file = upload_filed)
                    
                    if int(float(row['Hours'])) > 80 and leave_meta_obj.request_status:

                        try:
                            email_model.objects.get(leave_employee = leave_meta_obj)

                        except Exception  as e:
                            # if employee[0].dept and department_metadata.objects.select_related().filter(id = employee[0].dept.id).exists():
                            #     dept_obj = department_metadata.objects.select_related().filter(id = employee[0].dept.id)
                            #     department_head_obj = department_head_model.objects.prefetch_related('department').filter(department = dept_obj[0])
                            #     email_model.objects.create(leave_employee = leave_meta_obj,department_head = department_head_obj[0],email_send_to = [department_head_obj[0].user.email])
                            super_emp_data = supervisor_metadata.objects.filter(employee_data_id = employee[0].id)
                            if super_emp_data[0].indirect_supervisor_metadata and super_emp_data[0].supervisor:
                                email_send_to  = [super_emp_data[0].indirect_supervisor_metadata.employee.work_email,super_emp_data[0].supervisor.work_email]
                                email_model.objects.create(leave_employee = leave_meta_obj,email_send_to = email_send_to)

                            elif super_emp_data[0].indirect_supervisor_metadata:
                                email_send_to  = [super_emp_data[0].indirect_supervisor_metadata.employee.work_email]
                                email_model.objects.create(leave_employee = leave_meta_obj,email_send_to = email_send_to)

                            elif super_emp_data[0].supervisor:
                                email_send_to  = [super_emp_data[0].supervisor.work_email]
                                email_model.objects.create(leave_employee = leave_meta_obj,email_send_to = email_send_to)

                            else:
                                pass
        return JsonResponse({'message':True})




def home(request):
    context = { 'title_name':'Leave Dashboard','home':True}

    return render(request,'home_page.html',context)




'''This functionality called when bar graph need to be loaded'''
def chart_view_function(request):
    data3 = []
    data4 = []
    data5 = []
    label = []
    
    delta = timedelta(days=1)
    period_leave = datetime.datetime.now().date() + relativedelta(weeks=+3)
    start_date = datetime.datetime.now().date()

    holiday_count = 0
    leave_count = 0
    # Convert dates to timezone-aware datetime objects
    start_date = timezone.make_aware(datetime.datetime.combine(start_date, datetime.time.min))
    period_leave = timezone.make_aware(datetime.datetime.combine(period_leave, datetime.time.max))
    if request.user.id in [1,2]:    
        # Get employees in the same department(s)
        emp_dept = employee_metadata.objects.prefetch_related('work_location').all().exclude(id__in = [579,704, 706, 582, 711, 585, 716, 718, 622, 688, 752, 633])
        total_emp_count = emp_dept.count()

        # Get all holiday data in advance for efficiency
        holidays = holiday_metadata.objects.filter(start_date__lte=period_leave, end_date__gte=start_date)
        
        while start_date <= period_leave:
            # Skip weekends
            if start_date.weekday() > 4:
                start_date += delta
                continue
            else:
                holiday_count = 0
                for emp in emp_dept:
                    work_locations = list(emp.work_location.all())
                    if work_locations:  # Check if work locations exist
                        first_location = work_locations[0]  # Get the first work location safely
                        if holidays.filter(country_id=first_location.id, start_date__lte=start_date, end_date__gte=start_date).exists():
                            holiday_count += 1

                # Count total leave for employees in this department on this date
                total_leave = leave_metadata.objects.filter(
                    start_date__date__lte=start_date,
                    end_date__date__gte=start_date,
                    request_status=True
                ).count()

                # Aggregate data for this day
                total = holiday_count + total_leave
                data3.append(total_emp_count - total)  # Employee available
                data4.append(total_leave)  # Employees on leave
                data5.append(holiday_count)  # Employees on holiday
                label.append(f'{start_date.strftime("%m/%d/%Y")}')
                
                start_date += delta  # Move to the next day

        # Prepare data for JSON response
        data = {
            "labels": label,
            'data1': data3,
            'data2': data4,
            'data3': data5,
            'total_emp': total_emp_count
        }

        return JsonResponse(data, safe=False)
    elif request.user.id in [-1]:
        user_get = User.objects.get(id=request.user.id)
        
        # Get all work location names for the user in a single query
        work_locations_id = list(
            employee_metadata.objects.filter(user_id=user_get.id)
            .values_list('work_location__name', flat=True)
        )

        # Get employees in the same department(s) efficiently
        emp_dept = employee_metadata.objects.prefetch_related('work_location').filter(
            work_location__name__in=work_locations_id
        )

        # Get total employee count
        total_emp_count = emp_dept.count()

        # Get all holiday data in advance for efficiency
        # holidays = holiday_metadata.objects.filter(start_date__lte=period_leave, end_date__gte=start_date)
        
        while start_date <= period_leave:
            # Skip weekends
            if start_date.weekday() > 4:
                start_date += delta
                continue
            else:
                holiday_count = 0
                for emp in emp_dept:
                    # Check if there is a holiday on this date for the employee's work location

                    if holiday_metadata.objects.filter(country__name__in = work_locations_id , start_date__lte=start_date, end_date__gte=start_date):
                        holiday_count += 1

                # Count total leave for employees in this department on this date
                total_leave = leave_metadata.objects.filter(
                    employee__work_location__name__in=work_locations_id,
                    start_date__date__lte=start_date,
                    end_date__date__gte=start_date,
                    request_status=True
                ).count()

                # Aggregate data for this day
                total = holiday_count + total_leave
                data3.append(total_emp_count - total)  # Employee available
                data4.append(total_leave)  # Employees on leave
                data5.append(holiday_count)  # Employees on holiday
                label.append(f'{start_date.strftime("%m/%d/%Y")}')
                
                start_date += delta  # Move to the next day

        # Prepare data for JSON response
        data = {
            "labels": label,
            'data1': data3,
            'data2': data4,
            'data3': data5,
            'total_emp': total_emp_count
        }
        return JsonResponse(data, safe=False)
    else:
        emp_id = indirect_supervisor(request)
        print(emp_id)

        emp_dept = employee_metadata.objects.prefetch_related('work_location').filter(
                                    id__in=emp_id
                                ).exclude(
                                    Q(work_location=None) & Q(user_id__in=[522])
                                    
                                )
        
        total_emp_count = emp_dept.count()

        work_locations_id = list(
        employee_metadata.objects.filter(id__in=emp_id)
        .values_list('work_location__name', flat=True)
    )

        while start_date <= period_leave:
            # Skip weekends
            if start_date.weekday() > 4:
                start_date += delta
                continue
            else:
                
                holiday_count = 0
                for emp in emp_dept:
                    # Check if there is a holiday on this date for the employee's work location

                    if holiday_metadata.objects.filter(country__name__in = work_locations_id , start_date__lte=start_date, end_date__gte=start_date):
                        holiday_count += 1

                # Count total leave for employees in this department on this date
                total_leave = leave_metadata.objects.filter(
                    employee__id__in=emp_id,
                    start_date__date__lte=start_date,
                    end_date__date__gte=start_date,
                    request_status=True
                ).count()

                print(f'total leave {total_leave}')
                # Aggregate data for this day
                total = holiday_count + total_leave
                data3.append(total_emp_count - total) if total_emp_count>total else data3.append(0)# Employee available
                data4.append(total_leave)  if holiday_count != total_emp_count else data4.append(0)# Employees on leave
                data5.append(holiday_count)  # Employees on holiday
                label.append(f'{start_date.strftime("%m/%d/%Y")}')
                
                start_date += delta  # Move to the next day

        # Prepare data for JSON response
        data = {
            "labels": label,
            'data1': data3,
            'data2': data4,
            'data3': data5,
            'total_emp': total_emp_count
        }
        return JsonResponse(data, safe=False)
                


            

class home_view(LoginRequiredMixin,TemplateView):
    template_name = 'home_page.html'

    def get(self,request,*args,**kwargs):

        #This if condition for admin view only..
        if  request.user.id in [1,2]:
            emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
            full_name = f'{emp_datas.first_name} {emp_datas.last_name}'

            context = { 'title_name':'Leave Dashboard','home':True,'full_name':full_name}

            period = datetime.datetime.now().date() + relativedelta(weeks=+3)
            last_week_date = period - relativedelta(weeks=3)

            # user_get = User.objects.get(id = request.user.id)
            # dept_id = employee_metadata.objects.get(user = user_get).dept.id
            leave_date = leave_metadata.objects.filter(start_date__date__lte = period,end_date__date__gte=datetime.datetime.now().date(),request_status=True).order_by('start_date')
            holiday_data = holiday_metadata.objects.filter(start_date__lte = period,end_date__gte=datetime.datetime.now().date()).order_by('start_date') 
            context['leave_data'] = leave_date
            context['holiday_data'] = holiday_data
            context['next_week_date'] = period
            '''Date label need to fix'''
            # label = [data. for data in leave_week]
            # Optimized Query for Employee Data
            emp_data = employee_metadata.objects.all().order_by('first_name')
            emp_data_title = emp_data.order_by('job_title')  # Avoids redundant DB call

            # Optimized Query for Supervisors
            emp_supervisor = supervisor_metadata.objects.select_related('supervisor').all().order_by('supervisor__first_name')

            # Deduplicate supervisors using a dictionary
            super_selected_dict = {}
            for emp_datas in emp_supervisor:
                if emp_datas.supervisor.id not in super_selected_dict:
                    super_selected_dict[emp_datas.supervisor.id] = emp_datas

            # Extract final list of unique supervisors
            super_selected = list(super_selected_dict.values())

            # Optimized Query for Departments
            dept_data = department_metadata.objects.all().order_by('dept_name')

            # Optimized Work Location Deduplication
            work_location_data = country_metadata.objects.exclude(id=9).order_by('name')

            # Remove duplicates using dictionary
            work_location = list({work.name: work for work in work_location_data}.values())

            # Optimize fetching unique work location names from employees
            country_value = sorted(
                set(
                    work_name
                    for emp in employee_metadata.objects.prefetch_related('work_location')
                    .exclude(id__in=[579])
                    for work_name in emp.work_location.values_list('name', flat=True)
                )
            )


            context['emp_supervisor'] =  super_selected
            context['dept_data'] = dept_data
            context['work_location'] = country_value
            context['emp_data'] = emp_data
            return render(request,self.template_name,context)
        elif request.user.id in [00]:
            emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
            full_name = f'{emp_datas.first_name} {emp_datas.last_name}'

            context = { 'title_name':'Leave Dashboard','home':True,'full_name':full_name}

            period = datetime.datetime.now().date() + relativedelta(weeks=+3)
            
            work_locations_id = list(
            employee_metadata.objects.filter(user_id=self.request.user.id)
            .values_list('work_location__name', flat=True)
                )

            # dept_id =emp_datas.work_location.id
            leave_date = leave_metadata.objects.filter(employee__work_location__name__in = work_locations_id ,start_date__date__lte = period,end_date__date__gte=datetime.datetime.now().date(),request_status=True).order_by('start_date')
            holiday_data = holiday_metadata.objects.filter(country__name__in = work_locations_id,start_date__lte = period,end_date__gte=datetime.datetime.now().date()).order_by('start_date') 
            context['leave_data'] = leave_date
            context['holiday_data'] = holiday_data
            context['next_week_date'] = period
            '''Date label need to fix'''
            # label = [data. for data in leave_week]
            # Optimized Query for Employee Data           

            # Optimized Query for Departments
            dept_data = department_metadata.objects.all().order_by('dept_name')

            # Get work locations, excluding ID 9
            work_location_data = country_metadata.objects.exclude(id=9).order_by('name')

            # Remove duplicates using dictionary
            work_location = list({work.name: work for work in work_location_data}.values())

            # Optimize fetching unique work location names from employees
            country_value = sorted(
                set(
                    work_name
                    for emp in employee_metadata.objects.prefetch_related('work_location')
                    .exclude(id__in=[579])
                    for work_name in emp.work_location.values_list('name', flat=True)
                )
            )

            context['dept_data'] = dept_data
            context['work_location'] = country_value

            return render(request,self.template_name,context)
        
        else:
            emp_obj_get = indirect_supervisor(request)
            super_emp = employee_metadata.objects.filter(id__in = emp_obj_get)
            emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
            full_name = f'{emp_datas.first_name} {emp_datas.last_name}'

            context = { 'title_name':'Leave Dashboard','home':True,'full_name':full_name}

            period = datetime.datetime.now().date() + relativedelta(weeks=+3)
            
            emp_list = list({i.id for i in super_emp})


            work_locations_id = list(
                        employee_metadata.objects.filter(id__in=emp_list)
                        .values_list('work_location__name', flat=True)


                            )
                        
            
                # dept_id =emp_datas.work_location.id
            # leave_date = leave_metadata.objects.filter(employee__work_location__name__in = work_locations_id ,start_date__date__lte = period,end_date__date__gte=datetime.datetime.now().date(),request_status=True).order_by('start_date')
            leave_date = leave_metadata.objects.filter(employee_id__in = emp_list ,start_date__date__lte = period,end_date__date__gte=datetime.datetime.now().date(),request_status=True).order_by('start_date')
            print(f'data on leave {leave_date}')
            
            holiday_data = holiday_metadata.objects.filter(country__name__in = work_locations_id,start_date__lte = period,end_date__gte=datetime.datetime.now().date()).order_by('start_date') 
            context['leave_data'] = leave_date
            context['holiday_data'] = holiday_data
            context['next_week_date'] = period
            '''Date label need to fix'''
            # label = [data. for data in leave_week]
            # Optimized Query for Employee Data           

            # Optimized Query for Departments
            # dept_data = department_metadata.objects.all().order_by('dept_name')
            dept_data = department_metadata.objects.filter(id__in = list({i.dept.id for i in super_emp}))


            # Get work locations, excluding ID 9
            work_location_data = country_metadata.objects.exclude(id=9).order_by('name')

            # Remove duplicates using dictionary
            work_location = list({work.name: work for work in work_location_data}.values())

            # Optimize fetching unique work location names from employees
            country_value = sorted(
                set(
                    work_name
                    for emp in employee_metadata.objects.filter(id__in=list({i.id for i in super_emp})).exclude(Q(work_location=None) & Q(user_id__in=[522]))
                    for work_name in emp.work_location.values_list('name', flat=True)
                )
            )

            context['dept_data'] = dept_data
            context['work_location'] = country_value

            return render(request,self.template_name,context)
            # try:
            #     indirectsupervisor_metadata.objects.select_related('employee').filter(employee__user_id = request.user.id)
            #     indirect = indirectsupervisor_metadata.objects.select_related('employee').filter(employee__user_id = request.user.id)
            #     super = supervisor_metadata.objects.select_related('indirect_supervisor_metadata').filter(indirect_supervisor_metadata_id = indirect[0].id)
            #     print(list({i.supervisor.id for i in super}))
            #     super_emp = supervisor_metadata.objects.select_related('supervisor').filter(supervisor_id__in = list({i.supervisor.id for i in super}))
            #     emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
            #     full_name = f'{emp_datas.first_name} {emp_datas.last_name}'

            #     context = { 'title_name':'Leave Dashboard','home':True,'full_name':full_name}

            #     period = datetime.datetime.now().date() + relativedelta(weeks=+3)
                
            #     emp_list = list({i.employee_data.id for i in super_emp})


            #     work_locations_id = list(
            #                 employee_metadata.objects.filter(id__in=emp_list)
            #                 .values_list('work_location__name', flat=True)


            #                     )
                            
                
            #      # dept_id =emp_datas.work_location.id
            #     # leave_date = leave_metadata.objects.filter(employee__work_location__name__in = work_locations_id ,start_date__date__lte = period,end_date__date__gte=datetime.datetime.now().date(),request_status=True).order_by('start_date')
            #     print(f'data on  {emp_list}')
            #     leave_date = leave_metadata.objects.filter(employee_id__in = emp_list ,start_date__date__lte = period,end_date__date__gte=datetime.datetime.now().date(),request_status=True).order_by('start_date')
            #     print(f'data on leave {leave_date}')
               
            #     holiday_data = holiday_metadata.objects.filter(country__name__in = work_locations_id,start_date__lte = period,end_date__gte=datetime.datetime.now().date()).order_by('start_date') 
            #     context['leave_data'] = leave_date
            #     context['holiday_data'] = holiday_data
            #     context['next_week_date'] = period
            #     '''Date label need to fix'''
            #     # label = [data. for data in leave_week]
            #     # Optimized Query for Employee Data           

            #     # Optimized Query for Departments
            #     # dept_data = department_metadata.objects.all().order_by('dept_name')
            #     dept_data = department_metadata.objects.filter(id__in = list({i.employee_data.dept.id for i in super_emp}))


            #     # Get work locations, excluding ID 9
            #     work_location_data = country_metadata.objects.exclude(id=9).order_by('name')

            #     # Remove duplicates using dictionary
            #     work_location = list({work.name: work for work in work_location_data}.values())

            #     # Optimize fetching unique work location names from employees
            #     country_value = sorted(
            #         set(
            #             work_name
            #             for emp in employee_metadata.objects.filter(id__in=list({i.employee_data.id for i in super_emp})).exclude(Q(work_location=None) & Q(user_id__in=[522]))
            #             for work_name in emp.work_location.values_list('name', flat=True)
            #         )
            #     )

            #     context['dept_data'] = dept_data
            #     context['work_location'] = country_value

            #     return render(request,self.template_name,context)


            # except Exception as e:
            #     print('inisd e')
            #     super_emp = supervisor_metadata.objects.select_related('supervisor').filter(supervisor__user_id = request.user.id)
            #     emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
            #     full_name = f'{emp_datas.first_name} {emp_datas.last_name}'

            #     context = { 'title_name':'Leave Dashboard','home':True,'full_name':full_name}

            #     period = datetime.datetime.now().date() + relativedelta(weeks=+3)
                
            #     emp_list = list({i.employee_data.id for i in super_emp})
            #     work_locations_id = list(
            #                 employee_metadata.objects.filter(id__in=emp_list)
            #                 .values_list('work_location__name', flat=True)


            #                     )
                            
                
            #      # dept_id =emp_datas.work_location.id
            #     # leave_date = leave_metadata.objects.filter(employee__work_location__name__in = work_locations_id ,start_date__date__lte = period,end_date__date__gte=datetime.datetime.now().date(),request_status=True).order_by('start_date')
            #     leave_date = leave_metadata.objects.filter(employee_id__in = emp_list ,start_date__date__lte = period,end_date__date__gte=datetime.datetime.now().date(),request_status=True).order_by('start_date')
            #     print(f'employee leave {leave_date}')
               
            #     holiday_data = holiday_metadata.objects.filter(country__name__in = work_locations_id,start_date__lte = period,end_date__gte=datetime.datetime.now().date()).order_by('start_date') 
            #     context['leave_data'] = leave_date
            #     context['holiday_data'] = holiday_data
            #     context['next_week_date'] = period
            #     '''Date label need to fix'''
            #     # label = [data. for data in leave_week]
            #     # Optimized Query for Employee Data           

            #     # Optimized Query for Departments
            #     # dept_data = department_metadata.objects.all().order_by('dept_name')
            #     dept_data = department_metadata.objects.filter(id__in = list({i.employee_data.dept.id for i in super_emp}))

            #     # Get work locations, excluding ID 9
            #     work_location_data = country_metadata.objects.exclude(id=9).order_by('name')

            #     # Remove duplicates using dictionary
            #     work_location = list({work.name: work for work in work_location_data}.values())

            #     # Optimize fetching unique work location names from employees
            #     country_value = sorted(
            #         set(
            #             work_name
            #             for emp in employee_metadata.objects.filter(id__in=list({i.employee_data.id for i in super_emp})).exclude(Q(work_location=None) & Q(user_id__in=[522]))
            #             for work_name in emp.work_location.values_list('name', flat=True)
            #         )
            #     )

            #     context['dept_data'] = dept_data
            #     context['work_location'] = country_value

            #     return render(request,self.template_name,context)



    

class holiday_upload(TemplateView):
    template_name='holiday.html'

    def get(self,request):
        return render(request,self.template_name)
    

    def post(self,request):

        excel_file =self.request.FILES['holiday_file']
    
        # df = pd.read_excel(excel_file, header=0, skiprows=7)
        df = pd.read_excel(excel_file)

        df = df.fillna('') 
        for index, row in df.iterrows():

            if row['Country'] == 'USA':
                country_data = country_metadata.objects.filter(name ='USA')
            else:
                country_data = country_metadata.objects.filter(name = row['Country'], city = row['Region'] if row['Region'] else None)

            if len(holiday_metadata.objects.filter(country = country_data[0],holiday_name=row['Holiday'],start_date=row['Start Date'],year = 2025))==0:
                holiday_metadata.objects.create(country = country_data[0],holiday_name=row['Holiday'],
                                                start_date=row['Start Date'],end_date = row['End Date'],pto_days=row['PTO Days'],
                                                year = 2025)


        return HttpResponse('GOT IT')

import traceback   

class email_detail_post(TemplateView):

    template_name='holiday.html'
    def get(self,request):
        return render(request,self.template_name)
    


    def post(self, request):
        try:
            excel_file = request.FILES['holiday_file']
            df = pd.read_excel(excel_file).fillna('')

            for _, row in df.iterrows():
                user = self.get_or_create_user(row)
                city = self.get_work_location(row['Current Work Location Name'])
                department = self.get_or_create_department(row)
                employee = self.get_or_create_employee(user, row, city, department)
                indirect = self.get_or_create_indirect_supervisor(row)
                self.get_or_create_supervisor(row, employee, indirect)

            return HttpResponse('Data uploaded successfully.')

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e), 'trace': traceback.format_exc()}, status=500)

    def get_or_create_user(self, row):
        email = row['Current Work Email']
        user = User.objects.filter(email=email).first()
        if not user:
            username = f"{row['Preferred/First Name']}.{row['Last Name']}".lower().replace(" ", "")
            user = User.objects.create(
                first_name=row['Preferred/First Name'],
                last_name=row['Last Name'],
                username=username,
                email=email
            )
            user.set_password('Password#1')
            user.save()
        return user

    def get_work_location(self, location_name):
        work_location_mapping = {
            'C Space: Boston': 1,
            'C Space: Virtual - USA': 1,
            'New York Office': 1,
            'UK - C Space': 11,
            'Virtual - USA': 1,
            'UK - Escalent': 11,
            'PEO - New Zealand': 15,
        }
        city_id = work_location_mapping.get(location_name)
        return country_metadata.objects.get(id=city_id) if city_id else None

    def get_or_create_department(self, row):
        dept = department_metadata.objects.filter(dept_code=row['Department Code']).first()
        if not dept:
            dept = department_metadata.objects.create(
                dept_name=row['Department'],
                dept_description=row['Department Description'],
                dept_code=row['Department Code']
            )
        return dept

    def get_or_create_employee(self, user, row, city, department):
        email = row['Current Work Email']
        emp = employee_metadata.objects.filter(work_email=email).first()

        if emp:
            emp.first_name = row['Preferred/First Name']
            emp.last_name = row['Last Name']
            emp.job_title = row['Job Title']
            emp.dept = department
            emp.save()

            if city:
                emp.work_location.set([city])  # ManyToManyField
        else:
            emp = employee_metadata.objects.create(
                user=user,
                employee_id=row['Employee Id'],
                first_name=row['Preferred/First Name'],
                last_name=row['Last Name'],
                work_email=email,
                job_title=row['Job Title'],
                dept=department
            )
            if city:
                emp.work_location.set([city])
        return emp


    def get_or_create_indirect_supervisor(self, row):
        first_name, last_name = self.split_name(row.get("Indirect Supervisor's Name (First Last)", ""))
        # first_name = row.get("Indirect Supervisor's First Name")
        # last_name = row.get("Indirect Supervisor's First Name")
        email = row.get("Indirect Supervisor Work Email", "")

        user = User.objects.filter(email=email).first()
        if not user:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name.replace(' ',''),
                email=email,
                username=f"{first_name}.{last_name}".lower()
            )
            user.set_password('Password#1')
            user.save()

        employee = employee_metadata.objects.filter(work_email=email).first()
        if not employee:
            employee = employee_metadata.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                work_email=email
            )

        indirect = indirectsupervisor_metadata.objects.filter(employee=employee).first()
        if not indirect:
            indirect = indirectsupervisor_metadata.objects.create(employee=employee)
        return indirect

    def get_or_create_supervisor(self, row, employee, indirect):
        first_name, last_name = self.split_name(row.get("Supervisor's Name (First Last)", ""))
        # first_name  = row.get("Supervisor", "").split(',')[0].replace(' ','') 
        # last_name  = row.get("Supervisor", "").split(',')[1].replace(' ','') 
        email = row.get("Supervisor's Work Email", "")
        emp_id = row.get("Supervisor's Employee Code", "")

        user = User.objects.filter(email=email).first()
        if not user:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name.replace(' ',''),
                email=email,
                username=f"{first_name}.{last_name}".lower()
            )
            user.set_password('Password#1')
            user.save()

        emp = employee_metadata.objects.filter(work_email=email).first()
        if not emp:
            emp = employee_metadata.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                work_email=email,
                employee_id=emp_id
            )

        if not supervisor_metadata.objects.filter(
            supervisor=emp,
            indirect_supervisor_metadata=indirect,
            employee_data=employee
        ).exists():
            supervisor_metadata.objects.create(
                indirect_supervisor_metadata=indirect,
                supervisor=emp,
                employee_data=employee
            )

    def split_name(self, full_name):
        parts = full_name.strip().split(' ', 1)
        return parts if len(parts) == 2 else (parts[0], '')


    # def post(self,reqest):
    #     excel_file =self.request.FILES['holiday_file']
        
    #         # df = pd.read_excel(excel_file, header=0, skiprows=7)
    #     df = pd.read_excel(excel_file)

    #     df = df.fillna('') 
    #     for index, row in df.iterrows():
    #         first_name = row['Preferred/First Name']
    #         last_name = row['Last Name']
    #         username = f'{first_name}.{last_name}'
    #         email = row['Current Work Email']
    #         emp_id = row['Employee Id']
    #         if len(User.objects.filter(employee_id = emp_id))>0:
    #             user = User.objects.select_related().filter(employee_id = emp_id)[0]


    #         else:

    #             user = User.objects.create(first_name =first_name,last_name=last_name,username= username)
    #             user.set_password('Password#1')
    #             user.save()
    #             user = User.objects.select_related().filter(employee_id = emp_id)[0]
    #         work_location = row['Current Work Location Name']
    #         if work_location == 'C Space: Boston':
    #             city = country_metadata.objects.get(id=1)

    #         elif work_location == 'C Space: Virtual - USA':
    #             city = country_metadata.objects.get(id=2)

    #         elif work_location == 'New York Office':
    #             city = country_metadata.objects.get(id=3)

    #         # elif work_location == 'Boston Office' or work_location == 'Livonia':
    #         #     city = country_metadata.objects.get(id=1)
    #         else:
    #             # print('inside of it ')
    #             # print(work_location)
    #             pass


    #         department_data = department_metadata.objects.filter(dept_code=row['Department Code'])
    #         if len(department_data)>0:
    #             department_value = department_data[0]
    #         else:
    #             department_value = department_metadata.objects.create(dept_name = row['Department'],
    #                                                                   dept_description = row['Department Description'],
    #                                                                   dept_code=row['Department Code'])
                
    #         title = row['Job Title']
    #         # print(first_name)
    #         # print(row['Employee Id'])
    #         if len(employee_metadata.objects.filter(work_email=email))>0:
    #             employee_data_value = employee_metadata.objects.filter(work_email=email)[0]
    #             employee_data_value.first_name = first_name
    #             employee_data_value.last_name = last_name
    #             employee_data_value.job_title = title
    #             employee_data_value.dept = department_value
    #             employee_data_value.save() 

    #         else:
    #             employee_data_value = employee_metadata.objects.create(user = user,employee_id=row['Employee Id'],
    #                                                          first_name=first_name,last_name=last_name,work_location=city,
    #                                                          work_email=email,job_title=title,dept =department_value)
            
    #         #From Here we need to uncomment the code.
    #         employee_data_value = employee_metadata.objects.filter(work_email=email)[0]
    #         indirect_first = row["Indirect Supervisor's Name (First Last)"].split(' ',1)[0]
    #         indirect_last = row["Indirect Supervisor's Name (First Last)"].split(' ',1)[1]
    #         indirect_email = row["Indirect Supervisor Work Email"]
            
    #         indirect_user = User.objects.filter(email = indirect_email)

    #         if len(indirect_user)>0:
    #             indirect_value = User.objects.filter(email = indirect_email)[0]
    #             if len(employee_metadata.objects.filter(work_email=indirect_email))> 0:
    #                 indirect_employee = employee_metadata.objects.filter(work_email=indirect_email)[0]

    #                 indirect = indirectsupervisor_metadata.objects.filter(employee = indirect_employee)
    #                 if len(indirect)>0:
    #                     indirect = indirect[0]
    #                 else:
    #                     indirect = indirectsupervisor_metadata.objects.create(employee=indirect_employee)


    #             else:

    #                 indirect_employee = employee_metadata.objects.create(user=indirect_value,first_name=indirect_first,
    #                                                              last_name=indirect_last,work_email=indirect_email)
                    
    #                 indirect = indirectsupervisor_metadata.objects.create(employee=indirect_employee)


    #         else:
    #             indirect_value = User.objects.create(first_name = indirect_first,last_name = indirect_last,email = indirect_email,
    #                                                  username = f'{indirect_first}.{indirect_last}')
            
                
    #             indirect_value.set_password('Password#1')
    #             indirect_value.save()

    #             indirect_employee = employee_metadata.objects.create(user=indirect_value,first_name=indirect_first,
    #                                                              last_name=indirect_last,work_email=indirect_email)
                

    #             indirect = indirectsupervisor_metadata.objects.create(employee=indirect_employee)

            
    #         supervisor_data_first_name = row["Supervisor's Name (First Last)"].split(' ',1)[0]
    #         supervisor_data_last_name = row["Supervisor's Name (First Last)"].split(' ',1)[1]
    #         supervisor_data_email = row["Supervisor's Work Email"]
    #         supervisor_data_emp_id =row["Supervisor's Employee Code"]
    #         supervisor_user = User.objects.filter(email = supervisor_data_email)
    #         if len(supervisor_user)>0:
    #             supervisor_value = User.objects.filter(email = supervisor_data_email)[0]
    #             if len(employee_metadata.objects.filter(work_email=supervisor_data_email))>0:
    #                 super_emp = employee_metadata.objects.filter(work_email=supervisor_data_email)[0]

    #                 super = supervisor_metadata.objects.filter(supervisor=super_emp,indirect_supervisor_metadata = indirect,employee_data = employee_data_value )
    #                 if len(super)==0:
    #                     super = supervisor_metadata.objects.create(indirect_supervisor_metadata = indirect,supervisor=super_emp,
    #                                            employee_data = employee_data_value )
                        


    #             else:
    #                 super_emp = employee_metadata.objects.create(user=supervisor_value,first_name=supervisor_data_first_name,
    #                                                              last_name=supervisor_data_last_name,work_email=supervisor_data_email,
    #                                                              employee_id = supervisor_data_emp_id)
                    
    #                 super = supervisor_metadata.objects.create(indirect_supervisor_metadata = indirect,supervisor=super_emp,
    #                                            employee_data = employee_data_value )
    #         else:
    #             supervisor_value = User.objects.create(first_name = supervisor_data_first_name,last_name = supervisor_data_last_name,email = supervisor_data_email,
    #                                                  username = f'{supervisor_data_first_name}.{supervisor_data_last_name}')
                
    #             supervisor_value.set_password('Password#1')
    #             supervisor_value.save()

    #             super_emp = employee_metadata.objects.create(user=supervisor_value,first_name=supervisor_data_first_name,
    #                                                              last_name=supervisor_data_last_name,work_email=supervisor_data_email,
    #                                                              employee_id = supervisor_data_emp_id)
                
    #             super = supervisor_metadata.objects.create(indirect_supervisor_metadata = indirect,supervisor=super_emp,
    #                                            employee_data = employee_data_value )
            

            

                




            

            


            




            


    #     # for group_name, df_group in df1_grouped:
    #     #     for row_index, row in df_group.iterrows():
    #     #         col = row['Project']
    #     #         # project_detail_data =project_detail_model.objects.get(project_name =col) if len(project_detail_model.objects.filter(project_name =col))>0 else project_detail_model.objects.create(project_name =col)
    #     #         project_details, created = project_detail_model.objects.get_or_create(project_name=col)  
    #     #         employee_name = row['Employee Name'].split(' ',1)
    #     #         employee_detail = employee_metadata.objects.filter(first_name=employee_name[0],last_name=employee_name[1])
    #     #         if len(employee_detail)>0:
    #     #             project_detail.objects.create(employee =employee_detail[0],project_name=project_details)



    #     return HttpResponse('HELLO GOT')
    


class supervisor_detail_post(TemplateView):

    template_name='holiday.html'
    def get(self,request):
        return render(request,self.template_name)

    def post(self,reqest):
        excel_file =self.request.FILES['holiday_file']
        
            # df = pd.read_excel(excel_file, header=0, skiprows=7)
        df = pd.read_excel(excel_file)

        df = df.fillna('') 
        count = 0
        for index, row in df.iterrows():
            first_name = row['Preferred/First Name']
            last_name = row['Last Name']
            username = f'{first_name}.{last_name}'
            email = row['Work Email']
            employee_data_value = employee_metadata.objects.filter(work_email=email)[0]
            if employee_data_value:
                pass
            else:
                print(row['Work Email'])

            
            indirect_first = row["Indirect Supervisor's Name (First Last)"].split(' ',1)[0]
            indirect_last = row["Indirect Supervisor's Name (First Last)"].split(' ',1)[1]
            indirect_email = row["Indirect Supervisor's Work Email"]
            
            indirect_user = User.objects.filter(email = indirect_email)
            indirect = indirectsupervisor_metadata.objects.filter(employee__user = indirect_user[0])[0]

            # if len(indirect_user)>0:
            #     indirect_value = User.objects.filter(email = indirect_email)[0]
            #     if len(employee_metadata.objects.filter(work_email=indirect_email))> 0:
            #         indirect_employee = employee_metadata.objects.filter(work_email=indirect_email)[0]

            #         indirect = indirectsupervisor_metadata.objects.filter(employee = indirect_employee)
            #         if len(indirect)>0:
            #             indirect = indirect[0]
            #         else:
            #             indirect = indirectsupervisor_metadata.objects.create(employee=indirect_employee)


            #     else:

            #         indirect_employee = employee_metadata.objects.create(user=indirect_value,first_name=indirect_first,
            #                                                      last_name=indirect_last,work_email=indirect_email)
                    
            #         indirect = indirectsupervisor_metadata.objects.create(employee=indirect_employee)


            # else:
            #     indirect_value = User.objects.create(first_name = indirect_first,last_name = indirect_last,email = indirect_email,
            #                                          username = f'{indirect_first}.{indirect_last}')
            
                
            #     indirect_value.set_password('Password#1')
            #     indirect_value.save()

            #     indirect_employee = employee_metadata.objects.create(user=indirect_value,first_name=indirect_first,
            #                                                      last_name=indirect_last,work_email=indirect_email)
                

            #     indirect = indirectsupervisor_metadata.objects.create(employee=indirect_employee)

            
            supervisor_data_first_name = row["Supervisor's Name (First Last)"].split(' ',1)[0]
            supervisor_data_last_name = row["Supervisor's Name (First Last)"].split(' ',1)[1]
            supervisor_data_email = row["Supervisor's Work Email"]
            supervisor_data_emp_id =row["Supervisor's Employee ID"]
            supervisor_user = User.objects.filter(email = supervisor_data_email)
            super_emp = employee_metadata.objects.filter(work_email=supervisor_data_email)
            super = supervisor_metadata.objects.filter(supervisor=super_emp[0],indirect_supervisor_metadata=indirect,
                                                      employee_data =  employee_data_value)

            count = count+1

            if len(super)==0:
                supervisor_metadata.objects.create(supervisor=super_emp[0],indirect_supervisor_metadata=indirect,
                                                      employee_data =  employee_data_value)

            # if len(supervisor_user)>0:
            #     supervisor_value = User.objects.filter(email = supervisor_data_email)[0]
            #     if len(employee_metadata.objects.filter(work_email=supervisor_data_email))>0:
            #         super_emp = employee_metadata.objects.filter(work_email=supervisor_data_email)[0]

            #         super = supervisor_metadata.objects.filter(supervisor=super_emp)
            #         if len(super)==0:
            #             super = supervisor_metadata.objects.create(indirect_supervisor_metadata = indirect,supervisor=super_emp,
            #                                    employee_data = employee_data_value )
                        


            #     else:
            #         super_emp = employee_metadata.objects.create(user=supervisor_value,first_name=supervisor_data_first_name,
            #                                                      last_name=supervisor_data_last_name,work_email=supervisor_data_email,
            #                                                      employee_id = supervisor_data_emp_id)
                    
            #         super = supervisor_metadata.objects.create(indirect_supervisor_metadata = indirect,supervisor=super_emp,
            #                                    employee_data = employee_data_value )
            # else:
            #     supervisor_value = User.objects.create(first_name = supervisor_data_first_name,last_name = supervisor_data_last_name,email = supervisor_data_email,
            #                                          username = f'{supervisor_data_first_name}.{supervisor_data_last_name}')
                
            #     supervisor_value.set_password('Password#1')
            #     supervisor_value.save()

            #     super_emp = employee_metadata.objects.create(user=supervisor_value,first_name=supervisor_data_first_name,
            #                                                      last_name=supervisor_data_last_name,work_email=supervisor_data_email,
            #                                                      employee_id = supervisor_data_emp_id)
                
            #     super = supervisor_metadata.objects.create(indirect_supervisor_metadata = indirect,supervisor=super_emp,
            #                                    employee_data = employee_data_value )
            
            # print(super)

            



        return HttpResponse('HELLO GOT')
    


class project_detail_post(TemplateView):

    template_name='holiday.html'
    def get(self,request):
        return render(request,self.template_name)

    def post(self,reqest):
        excel_file =self.request.FILES['holiday_file']
        
            # df = pd.read_excel(excel_file, header=0, skiprows=7)
        df = pd.read_excel(excel_file)
        
        df1_grouped = df.groupby('Client')
        for group_name, df_group in df1_grouped:
            for row_index, row in df_group.iterrows():
                col = row['Client']
                # project_detail_data =project_detail_model.objects.get(project_name =col) if len(project_detail_model.objects.filter(project_name =col))>0 else project_detail_model.objects.create(project_name =col)
                project_details, created = project_detail_model.objects.get_or_create(project_name=col)
                # project_detail = project_detail_model.objects.get(project_name=col)
                employee_name = row['Employee Name'].split(' ',1)
                employee_detail = employee_metadata.objects.filter(first_name__icontains=employee_name[0],last_name__icontains=employee_name[1])
                if len(employee_detail)>0:
                    project_detail.objects.create(employee =employee_detail[0],project_name=project_details)



        return HttpResponse('HELLO GOT')
    

class project_detail_fetch_function(TemplateView):
    template_name = 'emp_list.html'
    def get(self,request,*args,**kwargs):
        id = self.request.GET.get('project_id')
        data = project_detail_model.objects.get(id=id)

        project_data = data.project_detail_set.all()

        employee_data = employee_metadata.objects.select_related().all().order_by('first_name')
        context = {'emp_data':employee_data,'project_data':project_data}

        return render(request,self.template_name,context)
    


class new_exisiting_project(TemplateView):

    def get(self,request,*args,**kwargs):

        if self.request.GET.get('new_project'):
            employee_data = employee_metadata.objects.select_related().all()
            context = {'employee_data':employee_data}
            return render(request,'new_project.html',context)
        else:
            project_detail_data = project_detail_model.objects.select_related().all()
            context = {'project_detail_data':project_detail_data}
            return render(request,'existing_project.html',context)




class add_project_view(TemplateView):
    def post(self,request,*args,**kwargs):
        data = request.POST
        emp_select = data.getlist('emp_select',None)
        emp_ID= []

        if emp_select:
            project_model_data = project_detail_model.objects.create(project_name = data.get('project_name'))
            for emp_data in emp_select:
                for value in emp_data.split(','):
                    employee_data = employee_metadata.objects.get(id=value)
                    project_detail.objects.create(project_name=project_model_data,employee=employee_data)



        return JsonResponse({'message':True})
    

class add_exiting_project_view(TemplateView):
    def post(self,request,*args,**kwargs):
        data = request.POST

        emp_select = data.getlist('emp_select',None)
        emp_ID= []

        if emp_select:

            project_model_data = project_detail_model.objects.get(id = data.get('project_name'))
            project_emp = project_detail.objects.filter(project_name = project_model_data)
            emp_data_present = [id.employee.id for id in project_emp] 

            for emp_data in emp_select:
                for value in emp_data.split(','):
                    employee_data = employee_metadata.objects.get(id=value)
                    emp_ID.append(employee_data.id)
                    # project_emp = project_detail.objects.filter(project_name = project_model_data)
                    # emp_id = 


            for data in emp_data_present:

                if data in emp_ID:
                    pass
                else:
                    employee_metadata.objects.get(id=data).delete()

            for data_value in emp_ID:
                project_details, created = project_detail.objects.get_or_create(project_name=project_model_data,
                                                                                      employee_id = data_value)




        return JsonResponse({'message':True})
    


class admin_view(LoginRequiredMixin,TemplateView):
    template_name = 'profile.html'

    def get(self,request,*args,**kwargs):
        emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
        full_name = f'{emp_datas.first_name} {emp_datas.last_name}'
        country_data =country_metadata.objects.select_related().all()[:1]
        starting_letter = emp_datas.first_name[0]
        context = {'title_name':'Profile','setting':True,'full_name':full_name,'emp_data':emp_datas,
                   'starting_letter':starting_letter,'country_data':country_data}

        # user_data = User.objects.get(id=self.request.user.id)
        # emp_data = employee_metadata,object(user = user_data)
        # context = {'emp_data':emp_data}

        return render(request,self.template_name,context)
    


class update_calendar(TemplateView):
    template_name = 'update_calendar.html'
    def post(self,request,*args,**kwargs):
        if request.user.id in [1,2]:
            data = request.POST

            emp_select = request.POST.getlist('emp_select',[]) #We need to provide the list of employee.
            department_selected = request.POST.getlist('departmentSelected')
            location_selected = request.POST.getlist('locationSelected')
            supervisor_select = request.POST.getlist('supervisorSelected')
            title_select = request.POST.getlist('titleSelect')

            # print(department_selected,location_selected,title_select)
            supervisor_select = [s for s in supervisor_select if s.strip().isdigit()]
            department_selected = [d for d in department_selected if d.strip().isdigit()]
            location_selected = [l for l in location_selected if l.strip()]
            title_select = [t for t in title_select if t.strip()]

            filters = Q()

            # Apply supervisor filter
            if supervisor_select:
                supervisor_emp_ids = supervisor_metadata.objects.filter(
                    supervisor_id__in=supervisor_select
                ).values_list('employee_data_id', flat=True)
                filters |= Q(id__in=supervisor_emp_ids)

            # Apply location filter
            if location_selected:
                filters |= Q(work_location__name__in=location_selected)

            # Apply department filter
            if department_selected:
                filters |= Q(dept_id__in=department_selected)

            # Apply job title filter
            if title_select:
                filters |= Q(job_title__in=title_select)

            # Final filtered employee queryset
            emp_data = employee_metadata.objects.prefetch_related('work_location').select_related('dept').filter(filters)

            # print(emp_data)
            

            select_date = data.get('date')
            start_date = datetime.datetime.strptime(data.get('date'), '%B %Y').strftime('%Y-%m-%d')
            end_date_data = datetime.datetime.strptime(start_date,'%Y-%m-%d')

            res = calendar.monthrange(end_date_data.year, end_date_data.month)
            end_date = f'{end_date_data.year}-{end_date_data.month}-{res[1]}'
            event = []
            emp_id = [i.id for i in emp_data]


            context = {
                'start_date':start_date,
                'select_date':select_date,
                'select_employee':emp_id
            }

            # for emp_data in emp_select:
            #     for value in emp_data.split(','):

            #         employee_data = employee_metadata.objects.get(id = value)
            #         emp_id.append(employee_data.id)


            for data_value in emp_data:
                # leave_data = leave_metadata.objects.select_related().filter(employee_id=employee_data.id,start_date__lte=end_date,end_date__gte=start_date)
                leave_data = leave_metadata.objects.select_related().filter(employee_id=data_value,start_date__lte=end_date,end_date__gte=start_date,request_status=True)
                for data in leave_data:
                    event_data = {'title' :f'{data.employee.first_name} {data.employee.last_name}/ {data.hours}hrs',
                    'id':data.id,
                    'hr_off':f'{data.hours}hrs',
                    'start':data.start_date,
                    'end':data.end_date,
                    'backgroundColor':'#3788d8',
                    'textColor':'white !important',
                    'fontSize':'5px !important',}
                    event.append(event_data)
            return render(request,self.template_name,context)
        # return JsonResponse({'template':self.template_name,'event':event})

        else:
            emp_list_obj = indirect_supervisor(request)
            data = request.POST

            emp_select = request.POST.getlist('emp_select',[]) #We need to provide the list of employee.
            department_selected = request.POST.getlist('departmentSelected')
            location_selected = request.POST.getlist('locationSelected')
            supervisor_select = request.POST.getlist('supervisorSelected')
            title_select = request.POST.getlist('titleSelect')

            # print(department_selected,location_selected,title_select)
            supervisor_select = [s for s in supervisor_select if s.strip().isdigit()]
            department_selected = [d for d in department_selected if d.strip().isdigit()]
            location_selected = [l for l in location_selected if l.strip()]
            title_select = [t for t in title_select if t.strip()]

            filters = Q()

            # filters |= Q(id__in = emp_list_obj)
            # Apply supervisor filter
            if supervisor_select:
                supervisor_emp_ids = supervisor_metadata.objects.filter(
                    supervisor_id__in=supervisor_select
                ).values_list('employee_data_id', flat=True)
                filters |= Q(id__in=supervisor_emp_ids)

            # Apply location filter
            if location_selected:
                filters |= Q(work_location__name__in=location_selected)

            # Apply department filter
            if department_selected:
                filters |= Q(dept_id__in=department_selected)

            # Apply job title filter
            if title_select:
                filters |= Q(job_title__in=title_select)

            # Final filtered employee queryset
            emp_data = employee_metadata.objects.prefetch_related('work_location').select_related('dept').filter(id__in = emp_list_obj).filter(filters)

            # print(emp_data)
            

            select_date = data.get('date')
            start_date = datetime.datetime.strptime(data.get('date'), '%B %Y').strftime('%Y-%m-%d')
            end_date_data = datetime.datetime.strptime(start_date,'%Y-%m-%d')

            res = calendar.monthrange(end_date_data.year, end_date_data.month)
            end_date = f'{end_date_data.year}-{end_date_data.month}-{res[1]}'
            event = []
            emp_id = [i.id for i in emp_data]


            context = {
                'start_date':start_date,
                'select_date':select_date,
                'select_employee':emp_id
            }

            # for emp_data in emp_select:
            #     for value in emp_data.split(','):

            #         employee_data = employee_metadata.objects.get(id = value)
            #         emp_id.append(employee_data.id)


            for data_value in emp_data:
                # leave_data = leave_metadata.objects.select_related().filter(employee_id=employee_data.id,start_date__lte=end_date,end_date__gte=start_date)
                leave_data = leave_metadata.objects.select_related().filter(employee_id=data_value,start_date__lte=end_date,end_date__gte=start_date,request_status=True)
                for data in leave_data:
                    event_data = {'title' :f'{data.employee.first_name} {data.employee.last_name}/ {data.hours}hrs',
                    'id':data.id,
                    'hr_off':f'{data.hours}hrs',
                    'start':data.start_date,
                    'end':data.end_date,
                    'backgroundColor':'#3788d8',
                    'textColor':'white !important',
                    'fontSize':'5px !important',}
                    event.append(event_data)
            return render(request,self.template_name,context)



# def update_calendar_js(request,date,emp,*args,**kwargs):
#     print('hello')
#     print(request.GET.get(date))
#     print('hbejbwjebjw')

#     return JsonResponse({'message':True})

class update_calendar_js(TemplateView):
    def get(self,request,*args,**kwargs):
        date = kwargs.get('date')
        emp_data = kwargs.get('emp')

        import ast
        start_date = datetime.datetime.strptime(date, '%B %Y').strftime('%Y-%m-%d')
        end_date_data = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        res = calendar.monthrange(end_date_data.year, end_date_data.month)
        end_date = f'{end_date_data.year}-{end_date_data.month}-{res[1]}'
        planned= []
        for value in ast.literal_eval(emp_data):
            employee_data = employee_metadata.objects.get(id = value)
            # leave_data = leave_metadata.objects.select_related().filter(employee_id=employee_data,start_date__lte=end_date,end_date__gte=start_date)
            leave_data = leave_metadata.objects.select_related().filter(employee_id=employee_data,request_status=True)
            for data in leave_data:
                event_data = {'title' :f'{data.employee.first_name} {data.employee.last_name}/ {data.hours}hrs',
                'id':f'{data.start_date.date()}',
                'hr_off':f'{data.hours}hrs',
                'start':data.start_date,
                'end':data.end_date,
                'backgroundColor':'#3788d8',
                'textColor':'white !important',
                'fontSize':'5px !important',}
                planned.append(event_data)


        return JsonResponse(planned,safe=False)
    

class supervisor_select(TemplateView):
    template_name = 'filter.html'
    def get(self,request,*args,**kwargs):
        data = self.request.GET
        emp_supervisor = supervisor_metadata.objects.select_related().all()
        super_id = []
        super_selected = []
        for emp_datas in emp_supervisor:
            if emp_datas.supervisor.id not in super_id:
                super_id.append(emp_datas.supervisor.id)
                super_selected.append(emp_datas)
        context = {}
        emp_data_select = []
        dept_data = []
        dept_data_id = []
        work_location_data = []
        work_location_data_id = []
        sup_final = []
        data_list = request.GET.getlist('super_value[]')
        job_tile = []
        project_list = []
        project_list_id = []

        
        for data in data_list:
            # sup_data = supervisor_metadata.objects.select_related().get(supervisor_id=data)
            emp_data = supervisor_metadata.objects.select_related().filter(supervisor_id =data)
            sup_final.append(emp_data[0].supervisor.id)
            
            for d_emp in emp_data:
                emp_data_select.append(d_emp)
        

        for data in  emp_data_select:
            if data.employee_data.dept.id not in dept_data_id:

                dept_data_id.append(data.employee_data.dept.id)
                dept_data.append(data.employee_data.dept)


            if data.employee_data.work_location.id not in work_location_data_id:
                work_location_data_id.append(data.employee_data.work_location.id)
                work_location_data.append(data.employee_data.work_location)
            # work_location_data.append(data.employee_data.work_location)
            job_tile.append(data.employee_data.job_title)
            for project_data in project_detail.objects.select_related().filter(employee_id = data.employee_data.id):
                if project_data.project_name.id not in project_list_id:
                    project_list_id.append(project_data.project_name.id)
                    project_list.append(project_data.project_name)




        
        
        job_title = list({val for val in job_tile})         
        context['emp_supervisor'] = super_selected
        context['sup_final'] = sup_final
        context['emp_data'] = emp_data_select
        context['dept_data'] = dept_data
        context['work_location'] = work_location_data
        context['job_title'] = job_title
        context['project_data'] = project_list
        return render(request,self.template_name,context)
        # return JsonResponse({'message':True})



class supervisor_select1(TemplateView):
    template_name = 'filter.html'
    def get(self,request,*args,**kwargs):
        data = self.request.GET
        # print(data)
        emp_supervisor = supervisor_metadata.objects.select_related().all().order_by('supervisor__first_name')
        super_id = []
        super_selected = []
        context = {}
        emp_data_select = []
        dept_data = []
        dept_data_id = []
        work_location_data = []
        work_location_data_id = []
        sup_final = []
        data_list = request.GET.getlist('super_value[]')
        job_tile = []
        project_list = []
        project_list_id = []

        title_emp_list = []

        job_title_id = []

        job_titles = []
        pro_emp_id = []

        pro_emp = []

        fetch_emp = []



        if data.get('emp_value') != 'false':
            fetch_emp = [i.id for i in employee_metadata.objects.select_related().filter(id__in = data.getlist('emp_value[]'))]

        if data.get('title_select') != 'false':
            title_fetch = request.GET.getlist('title_select[]')
            title_emp = employee_metadata.objects.select_related().filter(job_title__in = title_fetch).order_by('first_name')
            for tit in title_emp:
                title_emp_list.append(tit.id)
                if tit.job_title not in job_title_id:
                    job_title_id.append(tit.job_title)
                    job_titles.append(tit.job_title)

        if data.get('project_value') != 'false':
            for data in data.getlist('project_value[]'):
                project_detail_data = project_detail.objects.select_related().filter(project_name_id =data).order_by('employee__first_name')
                for value in project_detail_data:
                    # projects.append(value)
                    if value.project_name.id not in project_list_id:
                        project_list_id.append(value.project_name.id)
                        project_list.append(value.project_name)
                    if value.employee.id not in pro_emp_id:
                        pro_emp_id.append(value.employee.id)
                        pro_emp.append(value.employee.id)

        
        if data.get('dept_value') != 'false':
            for dept_val in department_metadata.objects.select_related().filter(id__in = data.getlist('dept_value[]')):
                if dept_val.id not in dept_data_id:
                    dept_data_id.append(dept_val.id)
                    dept_data.append(dept_val)


        
        if data.get('location_value') != 'false':
            for dept_val in country_metadata.objects.select_related().filter(name__in = data.getlist('location_value[]')):
                if dept_val.name not in work_location_data_id:
                    work_location_data_id.append(dept_val.name)
                    work_location_data.append(dept_val.namel)





        for emp_datas in emp_supervisor:
            if emp_datas.supervisor.id not in super_id:
                super_id.append(emp_datas.supervisor.id)
                super_selected.append(emp_datas)


        sup_selected_list = []
        sup_selected_id = []
        sup_employee_id = []
        sup_employee_list = []
        
        sup_data = supervisor_metadata.objects.select_related().filter(supervisor_id__in=data_list).order_by('employee_data__first_name')


        for sup_i in sup_data:
            if sup_i.supervisor.id not in sup_selected_id:
                sup_selected_id.append(sup_i.supervisor.id)
                sup_selected_list.append(sup_i)
            
            if sup_i.employee_data.id not in sup_employee_id:
                sup_employee_id.append(sup_i.employee_data.id)
                sup_employee_list.append(sup_i)




        if len(pro_emp)>0:
            sup_employee_id = list(set(pro_emp)&set(sup_employee_id))

        if len(title_emp_list)>0:
            sup_employee_id = list(set(title_emp_list)&set(sup_employee_id))

        
        # if len(fetch_emp)>0:
        #     sup_employee_id = list(set(fetch_emp)&set(sup_employee_id))

 
        for datas in  employee_metadata.objects.select_related().filter(id__in = sup_employee_id).order_by('first_name'):
            emp_data_select.append(datas)
            if data.get('dept_value') == 'false':
                if datas.dept and datas.dept.id not in dept_data_id:
                    dept_data_id.append(datas.dept.id)
                    dept_data.append(datas.dept)

            if data.get('location_value') == 'false':
                for work_loc in datas.work_location.all():  # Iterate through all related work locations
                    if work_loc.name not in work_location_data_id:
                        work_location_data_id.append(work_loc.name)
                        work_location_data.append(work_loc)


            # if datas.work_location.id not in work_location_data_id:
            #     work_location_data_id.append(datas.work_location.id)
                # work_location_data.append(datas.work_location)
            # work_location_data.append(data.employee_data.work_location)


            if len(job_titles) == 0:
                job_tile.append(datas.job_title)


            if data.get('project_value') == 'false':
                for project_data in project_detail.objects.select_related().filter(employee_id = datas.id).order_by('employee__first_name'):
                    if project_data.project_name.id not in project_list_id:
                        project_list_id.append(project_data.project_name.id)
                        project_list.append(project_data.project_name)



        
        job_title = list({val for val in job_tile}) if len(job_titles) == 0 else job_titles 
        context['emp_supervisor'] = super_selected
        # context['sup_final'] = sup_final
        context['sup_final'] = sup_selected_list
        context['emp_data'] = emp_data_select
        # context['dept_data'] = dept_data
        context['work_location'] = work_location_data
        context['dept_data'] = dept_data
        context['job_title'] = sorted(job_title)
        context['project_data'] = project_list
        return render(request,self.template_name,context)



    
class emp_select_function1(TemplateView):

    template_name = 'employee_filter.html'
    def get(self,request,*args,**kwargs):
        data = self.request.GET
        # print(data)
        context = {}
        emp_data_select = []
        em_data_id = []
        dept_data = []
        dept_data_id = []
        work_location_data = []
        work_location_data_id = []
        sup_final = []
        sup_final_id = []
        sup_final_selected = []
        job_tile  = [] 
        sup_value_fetch =[]
        title_emp_list = []
        job_title_id = []
        job_titles = []
        pro_emp_id = []
        pro_emp = []
        project_list_id =[]
        project_list = []
        data_list = request.GET.getlist('emp-select[]')
        # emp_data  = employee_metadata.objects.select_related().all()


        if data.get('title_select') != 'false':
            title_fetch = request.GET.getlist('title_select[]')
            title_emp = employee_metadata.objects.select_related().filter(job_title__in = title_fetch)
            for tit in title_emp:
                title_emp_list.append(tit.id)
                if tit.job_title not in job_title_id:
                    job_title_id.append(tit.job_title)
                    job_titles.append(tit.job_title)

        if data.get('project_value') != 'false':
            for data in data.getlist('project_value[]'):
                project_detail_data = project_detail.objects.select_related().filter(project_name_id =data)
                for value in project_detail_data:
                    # projects.append(value)
                    if value.project_name.id not in project_list_id:
                        project_list_id.append(value.project_name.id)
                        project_list.append(value.project_name)
                    if value.employee.id not in pro_emp_id:
                        pro_emp_id.append(value.employee.id)
                        pro_emp.append(value.employee.id)

        
        if data.get('dept_value') != 'false':
            for dept_val in department_metadata.objects.select_related().filter(id__in = data.getlist('dept_value[]')):
                if dept_val.id not in dept_data_id:
                    dept_data_id.append(dept_val.id)
                    dept_data.append(dept_val)


        if data.get('location_value') != 'false':
            for dept_val in country_metadata.objects.select_related().filter(name__in = data.getlist('location_value[]')):
                if dept_val.name not in work_location_data_id:
                    work_location_data_id.append(dept_val.name)
                    work_location_data.append(dept_val.name)

        sup_emp = []
        data =  self.request.GET
        if data.get('super_value',None) !='false':
            sup_value_fetch = request.GET.getlist('super_value[]')
            for fetch in sup_value_fetch:
                sup_selected = supervisor_metadata.objects.select_related().filter(supervisor_id =fetch)
                for emp in sup_selected:
                    if emp.supervisor.id not in sup_final_id:
                        sup_final_id.append(emp.supervisor.id)
                        sup_final_selected.append(emp)
                    sup_emp.append(emp.employee_data.id)


        
        for value in employee_metadata.objects.select_related().filter(id__in = data_list).exclude(user_id__in = [522,527]):
            if value.id not in em_data_id:
                em_data_id.append(value.id)
                emp_data_select.append(value)
                job_tile.append(value.job_title)

            if self.request.GET.get('dept_value') == 'false':
                if value.dept and value.dept.id not in dept_data_id:
                    dept_data_id.append(value.dept.id)
                    dept_data.append(value.dept) 
            

        


            if self.request.GET.get('location_value') == 'false':
                for work_loc in value.work_location.all():  # Iterate through all related work locations
                    if work_loc.name not in work_location_data_id:
                        work_location_data_id.append(work_loc.name)
                        work_location_data.append(work_loc)


            if self.request.GET.get('project_value'):
                for project_data in project_detail.objects.select_related().filter(employee_id = value.id):
                    if project_data.id not in project_list_id:
                        project_list_id.append(project_data.id)
                        project_list.append(project_data)



        for value in supervisor_metadata.objects.select_related().filter(employee_data_id__in = data_list):
            if data.get('super_value') == 'false':
                if value.supervisor.id not in sup_final_id:
                    sup_final_id.append(value.supervisor.id)
                    sup_final_selected.append(value)
            




        emp_data_all = employee_metadata.objects.select_related().all().order_by('first_name')
        job_title = list({val for val in job_tile})        
        # context['emp_supervisor'] = super_selected
        context['sup_final'] = sup_final
        context['sup_final_selected'] = sup_final_selected
        context['emp_data_select'] = emp_data_select
        context['emp_data_all'] = emp_data_all
        # context['emp_data'] = emp_data
        # context['dept_data'] = dept_data
        # context['work_location'] = work_location_data
        context['dept_data'] = dept_data
        context['work_location'] =  work_location_data
        context['job_title'] = job_title if data.get('title_select') == 'false' else job_titles
        context['job_title'] = sorted(context['job_title'])
        context['project_data'] = sorted(project_list, key=lambda x: x.project_name.project_name)#project_list
        context['supversior_v'] = self.request.GET.get('super_value')
        return render(request,self.template_name,context)
    




'''Department Filter Function'''
class dept_select_function(TemplateView):

    template_name = 'dept_filter.html'
    def get(self,request,*args,**kwargs):
        data = self.request.GET
        context = {}
        emp_data_select = []
        em_data_id = []
        dept_select_data = []
        dept_data_id = []
        work_location_data = []
        work_location_data_id = []
        sup_final = []
        sup_final_id = []
        sup_final_selected = []
        job_tile  = [] 
        sup_value_fetch =[]
        title_emp_list = []
        job_title_id = []
        job_titles = []
        pro_emp_id = []
        pro_emp = []
        project_list_id =[]
        project_list = []
        data_list = request.GET.getlist('dept_value[]')
        dept_data = department_metadata.objects.select_related().all()

        if data.get('title_select') != 'false':
            title_fetch = request.GET.getlist('title_select[]')
            title_emp = employee_metadata.objects.select_related().filter(job_title__in = title_fetch)
            for tit in title_emp:
                title_emp_list.append(tit.id)
                if tit.job_title not in job_title_id:
                    job_title_id.append(tit.job_title)
                    job_titles.append(tit.job_title)

        if data.get('emp_value') != 'false':
            fetch_emp = [i.id for i in employee_metadata.objects.select_related().filter(id__in = data.getlist('emp_value[]'))]

        if data.get('project_value') != 'false':
            for data in data.getlist('project_value[]'):
                project_detail_data = project_detail.objects.select_related().filter(project_name_id =data)
                for value in project_detail_data:
                    # projects.append(value)
                    if value.project_name.id not in project_list_id:
                        project_list_id.append(value.project_name.id)
                        project_list.append(value.project_name)
                    if value.employee.id not in pro_emp_id:
                        pro_emp_id.append(value.employee.id)
                        pro_emp.append(value.employee.id)


        if data.get('location_value') != 'false':
            for dept_val in country_metadata.objects.select_related().filter(name__in = data.getlist('location_value[]')):
                if dept_val.name not in work_location_data_id:
                    work_location_data_id.append(dept_val.name)
                    work_location_data.append(dept_val.name)

        sup_emp = []

        data =  self.request.GET
        if data.get('super_value',None) !='false':
            sup_value_fetch = request.GET.getlist('super_value[]')
            for fetch in sup_value_fetch:
                sup_selected = supervisor_metadata.objects.select_related().filter(supervisor_id =fetch)
                for emp in sup_selected:
                    if emp.supervisor.id not in sup_final_id:
                        sup_final_id.append(emp.supervisor.id)
                        sup_final_selected.append(emp)
                    sup_emp.append(emp.employee_data.id)

        
        for dat in employee_metadata.objects.select_related('dept').filter(dept_id__in = data_list ):
            if dat.id not in em_data_id:
                    em_data_id.append(dat.id)
                    emp_data_select.append(dat)

            if dat.dept.id not in dept_data_id:
                dept_data_id.append(dat.dept.id)
                dept_select_data.append(dat.dept)


        

        if len(sup_emp)>0:
            em_data_id = list(set(sup_emp)&set(em_data_id))
        if len(pro_emp)>0:
            em_data_id = list(set(pro_emp)&set(em_data_id))

        if len(fetch_emp)>0:
            em_data_id = list(set(fetch_emp)&set(em_data_id))


        if data.get('super_value') =='false':
            for sup in supervisor_metadata.objects.select_related().filter(employee_data_id__in=em_data_id):
                if sup.supervisor.id not in sup_final_id:
                    sup_final_id.append(sup.supervisor.id)
                    sup_final_selected.append(sup)


        if data.get('project_value') == 'false':
            for value in project_detail.objects.select_related().filter(employee_id__in =em_data_id):
                if value.project_name.id not in project_list_id:
                    project_list_id.append(value.project_name.id)
                    project_list.append(value.project_name)



        
        if data.get('title_select') == 'false':
            for tit in employee_metadata.objects.select_related().filter(id__in=em_data_id):
                title_emp_list.append(tit.id)
                if tit.job_title not in job_title_id:
                    job_title_id.append(tit.job_title)
                    job_titles.append(tit.job_title)

        emp_select_id = []
        emp_data_select = []
        for value in employee_metadata.objects.select_related().filter(id__in = em_data_id):
            if value.id not in emp_select_id:
                emp_select_id.append(value.id)
                emp_data_select.append(value)


            if data.get('location_value') == 'false':
                if not any(val.id == 9 for val in value.work_location.all()):
                    for work_loc in value.work_location.all():
                        if work_loc.name not in work_location_data_id:
                            work_location_data_id.append(work_loc.name)
                            work_location_data.append(work_loc)

        
        job_title = list({val for val in job_tile})        
        context['sup_final'] = sorted(sup_final_selected, key=lambda x: x.supervisor.first_name) #sup_final_selected
        context['emp_data'] = sorted(emp_data_select, key=lambda x: x.first_name) #emp_data_select
        context['dept_data'] = dept_data
        context['dept_select_data'] = dept_select_data
        context['work_location'] = work_location_data
        context['job_title'] =  sorted(job_titles)
        context['project_data'] = sorted(project_list, key=lambda x: x.project_name)#project_list
        context['supversior_v'] = self.request.GET.get('super_value')
        return render(request,self.template_name,context)
    




'''Location Filter'''
class location_select_function(TemplateView):

    template_name = 'location_filter.html'
    def get(self,request,*args,**kwargs):
        data = self.request.GET
        # print(data)
        context = {}
        emp_data_select = []
        em_data_id = []
        dept_data = []
        dept_data_id = []
        work_location_data = []
        work_location_data_id = []
        sup_final = []
        sup_final_id = []
        sup_final_selected = []
        job_tile  = [] 
        sup_value_fetch =[]
        title_emp_list = []
        job_title_id = []
        job_titles = []
        pro_emp_id = []
        pro_emp = []
        project_list_id =[]
        project_list = []
        fetch_emp = []
        data_list = request.GET.getlist('location_value[]')
        # dept_data = department_metadata.objects.select_related().all()

        if data.get('title_select') != 'false':
            title_fetch = request.GET.getlist('title_select[]')
            title_emp = employee_metadata.objects.select_related().filter(job_title__in = title_fetch)
            for tit in title_emp:
                title_emp_list.append(tit.id)
                if tit.job_title not in job_title_id:
                    job_title_id.append(tit.job_title)
                    job_titles.append(tit.job_title)

        if data.get('emp_value') != 'false':
            fetch_emp = [i.id for i in employee_metadata.objects.select_related().filter(id__in = data.getlist('emp_value[]'))]

        if data.get('project_value') != 'false':
            for data in data.getlist('project_value[]'):
                project_detail_data = project_detail.objects.select_related().filter(project_name_id =data)
                for value in project_detail_data:
                    # projects.append(value)
                    if value.project_name.id not in project_list_id:
                        project_list_id.append(value.project_name.id)
                        project_list.append(value.project_name)
                    if value.employee.id not in pro_emp_id:
                        pro_emp_id.append(value.employee.id)
                        pro_emp.append(value.employee.id)

        sup_emp = []

        data =  self.request.GET
        if data.get('super_value',None) !='false':
            sup_value_fetch = request.GET.getlist('super_value[]')
            for fetch in sup_value_fetch:
                sup_selected = supervisor_metadata.objects.select_related().filter(supervisor_id =fetch)
                for emp in sup_selected:
                    if emp.supervisor.id not in sup_final_id:
                        sup_final_id.append(emp.supervisor.id)
                        sup_final_selected.append(emp)
                    sup_emp.append(emp.employee_data.id)


        if self.request.GET.get('dept_value') != 'false':
            for dept_val in department_metadata.objects.select_related().filter(id__in = data.getlist('dept_value[]')):
                if dept_val.id not in dept_data_id:
                    dept_data_id.append(dept_val.id)
                    dept_data.append(dept_val)


        
        for dat in employee_metadata.objects.prefetch_related('work_location').filter(work_location__name__in = data_list ):
            if dat.id not in em_data_id:
                    em_data_id.append(dat.id)
                    emp_data_select.append(dat)

        for country in country_metadata.objects.select_related().filter(name__in = data_list).order_by('name'):
            if country.name not in work_location_data_id:
                work_location_data_id.append(country.name)
                work_location_data.append(country)
     

            # if dat.dept.id not in dept_data_id:
            #     dept_data_id.append(dat.dept.id)
            #     dept_select_data.append(dat.dept)


        

        if len(sup_emp)>0:
            em_data_id = list(set(sup_emp)&set(em_data_id))
        if len(pro_emp)>0:
            em_data_id = list(set(pro_emp)&set(em_data_id))

        if len(fetch_emp)>0:
            em_data_id = list(set(fetch_emp)&set(em_data_id))


        if data.get('super_value') =='false':
            for sup in supervisor_metadata.objects.select_related().filter(employee_data_id__in= em_data_id):
                if sup.supervisor.id not in sup_final_id:
                    sup_final_id.append(sup.supervisor.id)
                    sup_final_selected.append(sup)


        if data.get('project_value') == 'false':
            for value in project_detail.objects.select_related().filter(employee_id__in = em_data_id):
                if value.project_name.id not in project_list_id:
                    project_list_id.append(value.project_name.id)
                    project_list.append(value.project_name)



        
        if data.get('title_select') == 'false':
            for tit in employee_metadata.objects.select_related().filter(id__in= em_data_id):
                title_emp_list.append(tit.id)
                if tit.job_title not in job_title_id:
                    job_title_id.append(tit.job_title)
                    job_titles.append(tit.job_title)


        # if self.request.GET.get('dept_value') = 'false':


        emp_selected_id = []
        emp_data_selected = []
        for value in employee_metadata.objects.select_related().filter(id__in = em_data_id):
            if value.id not in emp_selected_id:
                emp_selected_id.append(value.id)
                emp_data_selected.append(value)
            if self.request.GET.get('dept_value') == 'false':
                if value.dept and value.dept.id not in dept_data_id:
                    dept_data_id.append(value.dept.id)
                    dept_data.append(value.dept) 

        work_id = []
        work_selected_location = []
        work_selected_location_data = country_metadata.objects.select_related().exclude(id=9).order_by('name')
        for work in work_selected_location_data:
            if work.name not in work_id:
                work_id.append(work.name)
                work_selected_location.append(work)
        job_title = list({val for val in job_tile})        
        context['sup_final'] = sup_final_selected
        context['emp_data'] = emp_data_selected
        context['dept_data'] = dept_data
        # context['dept_select_data'] = dept_data
        context['work_location'] = work_location_data
        context['work_selected_location'] = work_selected_location
        context['job_title'] =  job_titles
        context['project_data'] = project_list
        context['supversior_v'] = self.request.GET.get('super_value')
        return render(request,self.template_name,context)




class project_select_function1(TemplateView):

    template_name = 'project_filter.html'
    def get(self,request,*args,**kwargs):
        data = self.request.GET
        context = {}
        emp_data_select = []
        emp_select_id = []
        dept_data = []
        dept_data_id = []
        work_location_data = []
        work_location_data_id = []
        sup_final = []
        sup_final_id = []
        job_tile = []
        job_titles = []
        job_title_id = []
        select_project = []
        select_project_id = []
        projects= []
        fetch_emp = []
        data_list = request.GET.getlist('project-select[]')
        project_data = project_detail_model.objects.select_related().all().order_by('project_name')
        sup_emp = []
        sup_filter = []
        title_emp_list = []
        
        # print(data)
        
        if data.get('emp_value') != 'false':
            fetch_emp = [i.id for i in employee_metadata.objects.select_related().filter(id__in = data.getlist('emp_value[]'))]

        if data.get('super_value') !='false':
            sup_value_fetch = request.GET.getlist('super_value[]')
            for fetch in sup_value_fetch:
                sup_selected = supervisor_metadata.objects.select_related().filter(supervisor_id =fetch)
                for emp in sup_selected:
                    if emp.supervisor.id not in sup_final_id:
                        sup_final_id.append(emp.supervisor.id)
                        sup_emp.append(emp.employee_data.id)
                        sup_filter.append(emp)


        if data.get('title_select') != 'false':
            title_fetch = request.GET.getlist('title_select[]')
            title_emp = employee_metadata.objects.select_related().filter(job_title__in = title_fetch)
            for tit in title_emp:
                title_emp_list.append(tit.id)
                if tit.job_title not in job_title_id:
                    job_title_id.append(tit.job_title)
                    job_titles.append(tit.job_title)

        
        if data.get('dept_value') != 'false':
            for dept_val in department_metadata.objects.select_related().filter(id__in = data.getlist('dept_value[]')):
                if dept_val.id not in dept_data_id:
                    dept_data_id.append(dept_val.id)
                    dept_data.append(dept_val)


        
        if data.get('location_value') != 'false':
            for dept_val in country_metadata.objects.select_related().filter(name__in = data.getlist('location_value[]')):
                if dept_val.name not in work_location_data_id:
                    work_location_data_id.append(dept_val.name)
                    work_location_data.append(dept_val.name)



        # print(sup_filter)

        for data in data_list:
            # sup_data = supervisor_metadata.objects.select_related().get(supervisor_id=data)

            project_detail_data = project_detail.objects.select_related().filter(project_name_id =data)

            for value in project_detail_data:
                # projects.append(value)
                if value.project_name.id not in select_project_id:
                    select_project_id.append(value.project_name.id)
                    select_project.append(value.project_name)
                projects.append(value)
        emp_id = []
        emp_id_present = []
        for project in projects:
            # emp = employee_metadata.objects.select_related().filter(id = project.employee.id)
            if project.employee.id not in emp_id_present:
                emp_id_present.append(project.employee.id)
                emp_id.append(project.employee.id)
        

        if len(sup_emp)>0:
            emp_id = list(set(sup_emp)&set(emp_id))

        if len(title_emp_list)>0:
            emp_id = list(set(title_emp_list)&set(emp_id))

        if len(fetch_emp)>0:
            emp_id = list(set(fetch_emp)&set(emp_id))


        supervisor = []
        

        for value in employee_metadata.objects.select_related().filter(id__in = emp_id):
            if value.id not in emp_select_id:
                emp_select_id.append(value.id)
                emp_data_select.append(value)
                if self.request.GET.get('dept_value') == 'false':
                    if value.dept and value.dept.id not in dept_data_id:
                        dept_data_id.append(value.dept.id)
                        dept_data.append(value.dept)
                if len(job_titles) == 0:
                    job_tile.append(value.job_title) 
                supervisor.append(supervisor_metadata.objects.select_related().get(employee_data=value))

            
                if self.request.GET.get('location_value') == 'false':
                    if value.work_location.id !=9 and value.work_location.name not in work_location_data_id:
                        work_location_data_id.append(value.work_location.name)
                        work_location_data.append(value.work_location)


            # if value.dept.id not in dept_data_id:

            #     dept_data_id.append(value.dept.id)
            #     dept_data.append(value.dept)


            # if value.work_location.id not in work_location_data_id:
            #     work_location_data_id.append(value.work_location.id)
            #     work_location_data.append(value.work_location)
            
        if len(sup_filter) == 0:
            for sup_select in supervisor:
                if sup_select.supervisor.id not in sup_final_id:
                    sup_final_id.append(sup_select.supervisor.id)
                    sup_filter.append(sup_select)

                

        project_list = []
        project_list_id = []                                                                                                            

        # for sup in sup_final:
        #     for project_data in project_detail.objects.select_related().filter(employee_id = sup.employee_data.id):
        #         if project_data.id not in project_list_id:
        #             project_list_id.append(project_data.id)
        #             project_list.append(project_data)

        job_title = list({val for val in job_tile})  if len(job_titles) == 0 else job_titles
        # context['emp_supervisor'] = super_selected
        context['sup_final'] = sorted(sup_filter, key=lambda x:x. supervisor.first_name)#sup_filter
        context['emp_data'] = sorted(emp_data_select, key=lambda x: x.first_name)#emp_data_select
        # context['dept_data'] = dept_data
        # context['work_location'] = work_location_data
        context['dept_data'] = dept_data
        context['work_location'] = work_location_data
        context['job_title'] = sorted(job_title)
        context['project_data'] = sorted(project_data, key=lambda x: x.project_name)#project_data
        context['select_project'] = select_project
        
        return render(request,self.template_name,context)
    

class title_select_function1(LoginRequiredMixin,TemplateView):

    template_name = 'title_filter.html'
    def get(self,request,*args,**kwargs):
        data = self.request.GET
        # print(data)
        context = {}
        emp_data_select = []
        emp_data_select_id = []
        dept_data = []
        dept_data_id = []
        work_location_data = []
        work_location_data_id = []
        sup_final = []
        sup_final_id = []
        job_tile = []
        title_selected = []
        sup_emp = []
        pro_emp = []
        pro_emp_id = []
        project_list = []
        project_list_id = []
        fetch_emp = []
        data_list = request.GET.getlist('title-select[]')
        dept_data_avail = department_metadata.objects.select_related().all().order_by('dept_name')

        if data.get('emp_value') != 'false':
            fetch_emp = [i.id for i in employee_metadata.objects.select_related().filter(id__in = data.getlist('emp_value[]'))]


        if data.get('super_value') !='false':
            sup_value_fetch = request.GET.getlist('super_value[]')
            for fetch in sup_value_fetch:
                sup_selected = supervisor_metadata.objects.select_related().filter(supervisor_id =fetch)
                for emp in sup_selected:
                    if emp.supervisor.id not in sup_final_id:
                        sup_final_id.append(emp.supervisor.id)
                        sup_final.append(emp)
                    sup_emp.append(emp.employee_data.id)

        if data.get('project_value') != 'false':
            for data in data.getlist('project_value[]'):
                project_detail_data = project_detail.objects.select_related().filter(project_name_id =data)
                for value in project_detail_data:
                    # projects.append(value)
                    if value.project_name.id not in project_list_id:
                        project_list_id.append(value.project_name.id)
                        project_list.append(value.project_name)
                    if value.employee.id not in pro_emp_id:
                        pro_emp_id.append(value.employee.id)
                        pro_emp.append(value.employee.id)


        if data.get('dept_value') != 'false':
            for dept_val in department_metadata.objects.select_related().filter(id__in = data.getlist('dept_value[]')):
                if dept_val.id not in dept_data_id:
                    dept_data_id.append(dept_val.id)
                    dept_data.append(dept_val)



        if data.get('location_value') != 'false':
            for dept_val in country_metadata.objects.select_related().filter(name__in = data.getlist('location_value[]')):
                if dept_val.name not in work_location_data_id:
                    work_location_data_id.append(dept_val.name)
                    work_location_data.append(dept_val.name)
        


        emp_id  = [i.id for i in employee_metadata.objects.select_related().filter(job_title__in=data_list)]
        # print(emp_id)


        if len(sup_emp)>0:
            emp_id = list(set(sup_emp)&set(emp_id))
        if len(pro_emp)>0:
            emp_id = list(set(pro_emp)&set(emp_id))

        if len(fetch_emp)>0:
            emp_id = list(set(fetch_emp)&set(emp_id))
            
        for vale in emp_id:
            for value in employee_metadata.objects.select_related().filter(id=vale):

                emp_data_select.append(value)
                title_selected.append(value.job_title)
                if data.get('dept_value') == 'false':
                    if value.dept and value.dept.id not in dept_data_id:
                        dept_data_id.append(value.dept.id)
                        dept_data.append(value.dept)
                
                if data.get('location_value') == 'false':
                    if not any(val.id == 9 for val in value.work_location.all()):
                        for work_loc in value.work_location.all():
                            if work_loc.name not in work_location_data_id:
                                work_location_data_id.append(work_loc.name)
                                work_location_data.append(work_loc)

                    # if datas.dept and datas.dept.id not in dept_data_id:
                    # dept_data_id.append(datas.dept.id)
                    # dept_data.append(datas.dept)



                # if value.dept.id not in dept_data_id:

                #     dept_data_id.append(value.dept.id)
                #     dept_data.append(value.dept)


                # if value.work_location.id not in work_location_data_id:
                #     work_location_data_id.append(value.work_location.id)
                #     work_location_data.append(value.work_location)

                job_tile.append(value.job_title)



        if len(sup_final)==0:
            for dat in emp_data_select:
                select_sup = supervisor_metadata.objects.select_related().filter(employee_data=dat)


                for sup in select_sup:
                    if sup.supervisor.id not in sup_final_id:
                        sup_final_id.append(sup.supervisor.id)
                        sup_final.append(sup)


        




        if len(project_list)==0:
            for sup in sup_final:
                for project_data in project_detail.objects.select_related().filter(employee_id = sup.employee_data.id):
                    if project_data.project_name.id not in project_list_id:
                        project_list_id.append(project_data.project_name.id)
                        project_list.append(project_data)

        
        emp_data_title = employee_metadata.objects.select_related().all().order_by('job_title')
        emp_data_title = list({value.job_title for value in emp_data_title if value.job_title is not None})

        job_title = list({val.job_title for val in employee_metadata.objects.select_related().all() if val.job_title is not None})   

        # context['emp_supervisor'] = super_selected
        context['sup_final'] = sorted(sup_final, key=lambda x: x.supervisor.first_name) #sup_final
        context['emp_data'] = sorted(emp_data_select, key=lambda x: x.first_name)  #emp_data_select
        # context['dept_data'] = dept_data
        context['dept_data'] = dept_data
        context['work_location'] = work_location_data
        context['emp_data_title'] = sorted(emp_data_title)
        context['job_title'] = sorted(job_title)
        context['project_data'] = sorted(project_list, key=lambda x: x.project_name.project_name)#project_list
        context['title_selected'] = list({value for value in title_selected})


        return render(request,self.template_name,context)



class resetpasswordview(View):
    def post(self,request,**kwargs):
        data = request.POST
        # print(data)
        old_password = data.get('old_password')
        new_password1 = data.get('new_password')
        new_password2 = data.get('confirm_password')
        user = authenticate(username=self.request.user.username, password=old_password)
        form = PasswordChangeForm(request.user, request.POST) 
        if user:
            if new_password1 and new_password2 and new_password1 != new_password2:
                # messages.error(self.request, 'The entered password did not match.')
                return JsonResponse({"message":False,'error_message':'The entered password did not match.'})
            else:
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(self.request, user)  # Important!
                    return JsonResponse({"message":True,'success_message':'Your password reset successfully.'})
 
 
        else:
            return JsonResponse({"message":False,'error_message':'Please use a correct password'})



class holiday_add(LoginRequiredMixin,TemplateView):
    def post(self,request,*args,**kwargs):
        data = request.POST
        date = datetime.datetime.strptime(data.get('date'), "%d/%m/%Y").strftime('%Y-%m-%d')
        holiday_metadata.objects.create(country_id = data.get('holiday_select'),holiday_name= data.get('holiday_name'),
                                        start_date = date,end_date = date,
                                        year = 2024)
        return JsonResponse({'message':True})
    

class logout_function(TemplateView):
    def get(self,request):
        logout(self.request)
        return redirect('login')
    


class clear_filter_function(TemplateView):
    template_name = 'clear_filter_form.html'

    def get(self,request,*args,**kwargs):
        if self.request.user.id in [1,2]:
            emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
            full_name = f'{emp_datas.first_name} {emp_datas.last_name}'
            emp_data = employee_metadata.objects.select_related().all().order_by('first_name')
            emp_data_title = employee_metadata.objects.select_related().all().order_by('job_title')
            emp_supervisor = supervisor_metadata.objects.select_related().all().order_by('supervisor__first_name')
            super_id = []
            super_selected = []
            for emp_datas in emp_supervisor:
                if emp_datas.supervisor.id not in super_id:
                    super_id.append(emp_datas.supervisor.id)
                    super_selected.append(emp_datas)
            dept_data = department_metadata.objects.select_related().all().order_by('dept_name')
            work_id = []
            work_location = []
            work_location_data = country_metadata.objects.select_related().exclude(id=9).order_by('name')
            for work in work_location_data:
                if work.name not in work_id:
                    work_id.append(work.name)
                    work_location.append(work)


            project_data = project_detail_model.objects.select_related().all().order_by('project_name')
            job_title = list({value.job_title  for value in emp_data_title if value.job_title is not None})


            context = {
                'title_name':'Calendar','time_off':True,'emp_data':emp_data,
                'emp_supervisor':super_selected,'dept_data':dept_data,
                'work_location':work_location,'project_data':project_data,
                'job_title':sorted(job_title),
                'full_name':full_name
            }

            return render(request,self.template_name,context)
        
        elif request.user.id in [-22]:

            user_get = User.objects.get(id=request.user.id)
        
            # Get department ids for the user
            dept_id = [emp.dept.id for emp in employee_metadata.objects.filter(user=user_get)]
            
            # Get employees in the same department(s)
            emp_dept = employee_metadata.objects.select_related().filter(dept_id__in=dept_id)
            emp_dept_id = [e.id for e in emp_dept]
            # total_emp_count = emp_dept.count()
            emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
            full_name = f'{emp_datas.first_name} {emp_datas.last_name}'
            emp_data = emp_dept
            emp_data_title = emp_dept.order_by('job_title')
            emp_supervisor = supervisor_metadata.objects.select_related().filter(employee_data_id__in = emp_dept_id).order_by('supervisor__first_name')
            super_id = []
            super_selected = []
            for emp_datas in emp_supervisor:
                if emp_datas.supervisor.id not in super_id:
                    super_id.append(emp_datas.supervisor.id)
                    super_selected.append(emp_datas)
            dept_data = department_metadata.objects.select_related().filter(id__in = [e.dept.id for e in emp_dept]).all().order_by('dept_name')
            work_id = []
            work_location = []
            work_location_data = country_metadata.objects.select_related().filter(id__in = [e.work_location.id for e in emp_dept]).exclude(id=9).order_by('name')
            for work in work_location_data:
                if work.name not in work_id:
                    work_id.append(work.name)
                    work_location.append(work)


            '''Project Detail Logic Need to implements'''
            project_data = [
                                data.project_name for data in project_detail.objects
                                .select_related('project_name')  # Pre-fetch related 'project_name'
                                .filter(employee_id__in=emp_dept)  # Filter based on emp_dept list
                                .order_by('project_name__project_name')  # Order by the 'name' field of the related project model
                            ]
            project_data = list(dict.fromkeys(project_data))
            job_title = list({value.job_title  for value in emp_data_title if value.job_title is not None})

            context = {
                'title_name':'Calendar','time_off':True,'emp_data':emp_data,
                'emp_supervisor':super_selected,'dept_data':dept_data,
                'work_location':work_location,'project_data':project_data,
                'job_title':sorted(job_title),
                'full_name':full_name
            }

            return render(request,self.template_name,context)
        
        else:
            emp_data_obj = indirect_supervisor(request)

            emp_datas = employee_metadata.objects.get(user_id = self.request.user.id)
            full_name = f'{emp_datas.first_name} {emp_datas.last_name}'
            emp_data = employee_metadata.objects.select_related().filter(id__in = emp_data_obj).exclude(
                                    Q(work_location=None) & Q(user_id__in=[522])
                                    
                                ).order_by('first_name')
            emp_data_title = employee_metadata.objects.select_related().filter(id__in = emp_data_obj).exclude(
                                    Q(work_location=None) & Q(user_id__in=[522])
                                    
                                ).order_by('first_name').order_by('job_title')
            emp_supervisor = supervisor_metadata.objects.select_related('supervisor').filter(employee_data_id__in = emp_data_obj).order_by('supervisor__first_name')
            super_id = []
            super_selected = []
            for emp_datas in emp_supervisor:
                if emp_datas.supervisor.id not in super_id:
                    super_id.append(emp_datas.supervisor.id)
                    super_selected.append(emp_datas)
            # dept_data = department_metadata.objects.select_related().all().order_by('dept_name')

            dept_data = department_metadata.objects.select_related().filter(id__in = [e.dept.id for e in emp_data]).order_by('dept_name')
            work_id = []
            work_location = []  



            #work_location_data = country_metadata.objects.select_related().exclude(id=9).order_by('name')

            work_locations_id = list(
                            employee_metadata.objects.filter(id__in=emp_data_obj)
                            .values_list('work_location__name', flat=True)


                                )
            

            work_location_data = country_metadata.objects.select_related().filter(name__in = work_locations_id).exclude(id=9).order_by('name')
            for work in work_location_data:
                if work.name not in work_id:
                    work_id.append(work.name)
                    work_location.append(work)


            project_data = project_detail_model.objects.select_related().all().order_by('project_name')
            job_title = list({value.job_title  for value in emp_data_title if value.job_title is not None})


            context = {
                'title_name':'Calendar','time_off':True,'emp_data':emp_data,
                'emp_supervisor':super_selected,'dept_data':dept_data,
                'work_location':work_location,'project_data':project_data,
                'job_title':sorted(job_title),
                'full_name':full_name
            }

            return render(request,self.template_name,context)
    

    





#This function used to find platform according to which it download in download folder
def get_desktop_path(file_name):
    # Get the current user's home directory
    user_profile = os.environ.get("USERPROFILE") or os.environ.get("HOME")
    
    if platform.system() == "Windows":
        desktop_path = os.path.join(user_profile, "Downloads")
    elif platform.system() == "Darwin":  # macOS
        desktop_path = os.path.join(user_profile, "Downloads")
    elif platform.system() == "Linux":
        desktop_path = os.path.join(user_profile, "Downloads")
    else:
        raise OSError("Unsupported operating system")
    
    return f"{file_name}.ics"
    # return os.path.join(desktop_path, f"{file_name}.ics")

class outlook_calendar_download(TemplateView):

    def get(self,request,*args,**kwargs):
        emp_data = request.GET.get('emp_data').split('/')[0].split(' ',1)
        # Combine it with the filename to get the full path
        full_name = f'{emp_data[0]}{emp_data[1]}'
        employee_val = employee_metadata.objects.filter(first_name__icontains = emp_data[0],last_name__icontains=emp_data[1])
        leave_data = leave_metadata.objects.filter(employee = employee_val[0],start_date = request.GET.get('date'),request_status=True)
        start_date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d").strftime("%Y%m%d")
        name = request.GET.get('emp_data')
        end_date = (leave_data[0].end_date+timedelta(days=1)).strftime("%Y%m%d")
        location = 'Out of office'
        desktop_path = get_desktop_path(full_name)
        my_files = desktop_path
        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
BEGIN:VEVENT
SUMMARY:{request.GET.get('emp_data')}
DTSTART:{start_date}
DTEND:{end_date}
LOCATION:{location}
DESCRIPTION:'Out of office'
STATUS:FREE
TRANSP:TRANSPARENT
BEGIN:VALARM
TRIGGER:-PT10M
DESCRIPTION:Reminder for {request.GET.get('emp_data')}
ACTION:DISPLAY
END:VALARM
END:VEVENT
END:VCALENDAR
        """
        with open(my_files, 'w') as my_file:
            my_file.write(ics_content)

        response = HttpResponse(ics_content,content_type = 'text/calendar')
        response['Content-Type'] = 'application/force-download'
        response["Content-Disposition"] = f'attachment;filename={my_files}'
        os.remove(my_files)
        # return JsonResponse({'message':True,'my_files':my_files})
        return response
    

#This function used to check the column available or not
def check_columns(df, required_columns):
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(missing_columns)}")
    else:
        print("All columns are present")

class bluk_project_upload(TemplateView):
    template_name = 'bluk_client.html'

    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)
    


    def post(self,request,*args,**kwargs):
        client_file_excel = self.request.FILES.get('bluk_file_upload_id')
        print(client_file_excel)
        df = pd.read_csv(client_file_excel)
        # Restore ManyToMany relationships
        for index, row in df.iterrows():
            print(row['employee_id'])
            try:
                employee = employee_metadata.objects.get(employee_id=row['employee_id'])
                country = country_metadata.objects.get(id=row['work_location_id'])
                employee.work_location.add(country)
                print(f"Restored: {employee.id} -> {country.id}")
            except Exception as e:
                print(f"Error restoring {row['employee_id']}: {e}")

        # df = pd.read_excel(client_file_excel)
        # required_columns = ['Employee Name', 'Client']
        
        # try:
        #     check_columns(df, required_columns)
        # except ValueError as e:
        #     print(e)
        #     return JsonResponse({'message':False,"error": str(e)})
        # df1_grouped = df.groupby('Client')
        # for group_name, df_group in df1_grouped:
        #     for row_index, row in df_group.iterrows():
        #         col = row['Client']
        #         # project_detail_data =project_detail_model.objects.get(project_name =col) if len(project_detail_model.objects.filter(project_name =col))>0 else project_detail_model.objects.create(project_name =col)
        #         project_details, created = project_detail_model.objects.get_or_create(project_name=col)
        #         # project_detail = project_detail_model.objects.get(project_name=col)
        #         employee_name = row['Employee Name'].split(' ',1)
        #         employee_detail = employee_metadata.objects.filter(first_name__icontains=employee_name[0],last_name__icontains=employee_name[1])
        #         if len(employee_detail)>0:
        #             project_detail.objects.create(employee =employee_detail[0],project_name=project_details)

        return JsonResponse({'message':True})



class employee_file_upload1(TemplateView):

    def post(self,request,*args,**kwargs):
        emp_upload_file = self.request.FILES.get('emps_file_upload')
        df = pd.read_excel(emp_upload_file)
        df = df.fillna('') 
        required_columns = ['Preferred/First Name', 'Last Name', 'Employee Id','Department Code',
                            'Department','Current Work Location Name',
                            'Job Title',"Supervisor's Employee Code","Supervisor's Name (First Last)"]
        
        try:
            check_columns(df, required_columns)
        except ValueError as e:
            print(e)
            return JsonResponse({'message':False,"error": str(e)})
        for index, row in df.iterrows():
            first_name = row['Preferred/First Name']
            last_name = row['Last Name']
            username = f'{first_name}.{last_name}'
            # email = row['Current Work Email']
            emp_id = row['Employee Id']

            if len(User.objects.select_related().filter(employee_id = emp_id))>0:
                user = User.objects.select_related().filter(employee_id = emp_id)[0]
            else:
                user = User.objects.create(first_name =first_name,last_name=last_name,username= username,
                                        employee_id = emp_id)
                user.set_password('Password#1')
                user.save()
                user = User.objects.select_related().filter(employee_id = emp_id)[0]

            work_location = row['Current Work Location Name']
            if work_location == 'C Space: Boston':
                city = country_metadata.objects.get(id=1)

            elif work_location == 'C Space: Virtual - USA':
                city = country_metadata.objects.get(id=2)

            elif work_location == 'New York Office':
                city = country_metadata.objects.get(id=3)

            # elif work_location == 'Boston Office' or work_location == 'Livonia':
            #     city = country_metadata.objects.get(id=1)
            else:
                # print('inside of it ')
                # print(work_location)
                pass


            department_data = department_metadata.objects.filter(dept_code=row['Department Code'])
            if len(department_data)>0:
                department_value = department_data[0]
            else:
                department_value = department_metadata.objects.create(dept_name = row['Department'],
                                                                      dept_description = row['Department Description'],
                                                                      dept_code=row['Department Code'])
                
            title = row['Job Title']
            email = row['Work Email']
            # print(first_name)
            # print(row['Employee Id'])
            if len(employee_metadata.objects.filter(work_email=email))>0:
                employee_data_value = employee_metadata.objects.filter(work_email=email)[0]

            else:
                employee_data_value = employee_metadata.objects.create(user = user,employee_id=row['Employee Id'],
                                                             first_name=first_name,last_name=last_name,work_location=city,
                                                             work_email=email,job_title=title,dept =department_value)
                

        for index, row in df.iterrows():

            # print(row['Current Work Email'])
            employee_data_value = employee_metadata.objects.filter(work_email=row['Current Work Email'])[0]
            indirect_first = row["Indirect Supervisor's Name (First Last)"].split(' ',1)[0]
            indirect_last = row["Indirect Supervisor's Name (First Last)"].split(' ',1)[1]
            indirect_email = row["Indirect Supervisor Work Email"]
            
            indirect_user = User.objects.filter(email = indirect_email)

            if len(indirect_user)>0:
                indirect_value = User.objects.filter(email = indirect_email)[0]
                if len(employee_metadata.objects.filter(work_email=indirect_email))> 0:
                    indirect_employee = employee_metadata.objects.filter(work_email=indirect_email)[0]

                    indirect = indirectsupervisor_metadata.objects.filter(employee = indirect_employee)
                    if len(indirect)>0:
                        indirect = indirect[0]
                    else:
                        indirect = indirectsupervisor_metadata.objects.create(employee=indirect_employee)


                else:

                    indirect_employee = employee_metadata.objects.create(user=indirect_value,first_name=indirect_first,
                                                                 last_name=indirect_last,work_email=indirect_email)
                    
                    indirect = indirectsupervisor_metadata.objects.create(employee=indirect_employee)


            else:
                indirect_value = User.objects.create(first_name = indirect_first,last_name = indirect_last,email = indirect_email,
                                                     username = f'{indirect_first}.{indirect_last}')
            
                
                indirect_value.set_password('Password#1')
                indirect_value.save()

                indirect_employee = employee_metadata.objects.create(user=indirect_value,first_name=indirect_first,
                                                                 last_name=indirect_last,work_email=indirect_email)
                

                indirect = indirectsupervisor_metadata.objects.create(employee=indirect_employee)

            
            supervisor_data_first_name = row["Supervisor's Name (First Last)"].split(' ',1)[0]
            supervisor_data_last_name = row["Supervisor's Name (First Last)"].split(' ',1)[1]
            supervisor_data_email = row["Supervisor's Work Email"]
            supervisor_data_emp_id =row["Supervisor's Employee Code"]
            supervisor_user = User.objects.filter(email = supervisor_data_email)
            if len(supervisor_user)>0:
                supervisor_value = User.objects.filter(email = supervisor_data_email)[0]
                if len(employee_metadata.objects.filter(work_email=supervisor_data_email))>0:
                    super_emp = employee_metadata.objects.filter(work_email=supervisor_data_email)[0]
                    if super_emp.employee_id == None:
                        super_emp.employee_id = supervisor_data_emp_id
                        super_emp.save()

                    super = supervisor_metadata.objects.filter(supervisor=super_emp,indirect_supervisor_metadata = indirect,employee_data = employee_data_value )
                    if len(super)==0:
                        super = supervisor_metadata.objects.create(indirect_supervisor_metadata = indirect,supervisor=super_emp,
                                               employee_data = employee_data_value )
                        


                else:
                    super_emp = employee_metadata.objects.create(user=supervisor_value,first_name=supervisor_data_first_name,
                                                                 last_name=supervisor_data_last_name,work_email=supervisor_data_email,
                                                                 employee_id = supervisor_data_emp_id)
                    
                    super = supervisor_metadata.objects.create(indirect_supervisor_metadata = indirect,supervisor=super_emp,
                                               employee_data = employee_data_value )
            else:
                supervisor_value = User.objects.create(first_name = supervisor_data_first_name,last_name = supervisor_data_last_name,email = supervisor_data_email,
                                                     username = f'{supervisor_data_first_name}.{supervisor_data_last_name}')
                
                supervisor_value.set_password('Password#1')
                supervisor_value.save()

                super_emp = employee_metadata.objects.create(user=supervisor_value,first_name=supervisor_data_first_name,
                                                                 last_name=supervisor_data_last_name,work_email=supervisor_data_email,
                                                                 employee_id = supervisor_data_emp_id)
                
                super = supervisor_metadata.objects.create(indirect_supervisor_metadata = indirect,supervisor=super_emp,
                                               employee_data = employee_data_value )


        return JsonResponse({'message':True})



'''Employee Upload functionality'''
class employee_file_upload(TemplateView):

    def post(self, request, *args, **kwargs):
        emp_upload_file = self.request.FILES.get('emps_file_upload')
        df = pd.read_excel(emp_upload_file).fillna('')  # Handle NaN values

        required_columns = ['Preferred/First Name', 'Last Name', 'Employee Id', 'Department Code',
                            'Department', 'Current Work Location Name', 'Job Title',
                            "Supervisor's Employee Code", "Supervisor's Name (First Last)"]

        try:
            check_columns(df, required_columns)
        except ValueError as e:
            print(e)
            return JsonResponse({'message': False, "error": str(e)})

        work_location_mapping = {
            'C Space: Boston': 1,
            'C Space: Virtual - USA': 2,
            'New York Office': 3,
            'UK - C Space': 11,
            'Virtual - USA':1,
            'C Space: Virtual - USA':1,
            'UK - Escalent':11,

        }

        for index, row in df.iterrows():
            first_name = row['Preferred/First Name']
            last_name = row['Last Name']
            emp_id = row['Employee Id']
            title = row['Job Title']
            work_location = row['Current Work Location Name']

            # Work Location Handling Optimization
            city = country_metadata.objects.filter(id=work_location_mapping.get(work_location)).first()
            if not city:
                city, _ = country_metadata.objects.get_or_create(name=work_location)

            # Department Handling Optimization
            department_value, _ = department_metadata.objects.get_or_create(
                dept_code=row['Department Code'],
                defaults={'dept_name': row['Department']}
            )

            # Employee Handling Optimization
            employee_data_value, created = employee_metadata.objects.get_or_create(
            employee_id=emp_id,
            defaults={'first_name': first_name, 'last_name': last_name, 'job_title': title, 'dept': department_value}
            )

            # Handle ManyToManyField separately after object creation
            if created:
                employee_data_value.work_location.set([city])  # Use .set() for ManyToManyField
            else:
                employee_data_value.first_name = first_name
                employee_data_value.last_name = last_name
                employee_data_value.job_title = title
                employee_data_value.dept = department_value
                employee_data_value.save()  

                # Update work_location (ManyToManyField)
                employee_data_value.work_location.clear()  # Remove old locations
                employee_data_value.work_location.add(city)  # Add the new location


            # Supervisor Handling
            supervisor_data = row["Supervisor's Name (First Last)"].split(' ', 1)
            supervisor_data_first_name = supervisor_data[0]
            supervisor_data_last_name = supervisor_data[1] if len(supervisor_data) > 1 else ''

            supervisor_data_emp_id = row["Supervisor's Employee Code"]

            super_emp, _ = employee_metadata.objects.get_or_create(
                employee_id=supervisor_data_emp_id,
                defaults={'first_name': supervisor_data_first_name, 'last_name': supervisor_data_last_name}
            )

            # Supervisor Metadata Handling
            supervisor_metadata.objects.get_or_create(employee_data=employee_data_value, supervisor=super_emp)

        return JsonResponse({'message': True})
    



class employee_file_uploads(TemplateView):

    def post(self, request, *args, **kwargs):
        emp_upload_file = self.request.FILES.get('emps_file_upload')
        df = pd.read_excel(emp_upload_file).fillna('')  # Handle NaN values

        required_columns = ['Preferred/First Name', 'Last Name', 'Employee Id', 'Department Code',
                            'Department', 'Current Work Location Name', 'Job Title',
                            "Supervisor's Employee Code", "Supervisor's Name (First Last)"]

        try:
            check_columns(df, required_columns)
        except ValueError as e:
            print(e)
            return JsonResponse({'message': False, "error": str(e)})

        work_location_mapping = {
            'C Space: Boston': 1,
            'C Space: Virtual - USA': 1,
            'New York Office': 1,
            'UK - C Space': 11,
            'Virtual - USA':1,
            'C Space: Virtual - USA':1,
            'UK - Escalent':11,
            'PEO - New Zealand':15,


        }

        for index, row in df.iterrows():
            first_name = row['Preferred/First Name']
            last_name = row['Last Name']
            emp_id = row['Employee Id']
            title = row['Job Title']
            work_location = row['Current Work Location Name']

            # Work Location Handling Optimization
            city = country_metadata.objects.filter(id=work_location_mapping.get(work_location)).first()
            if not city:
                city, _ = country_metadata.objects.get_or_create(name=work_location)

            # Department Handling Optimization
            department_value, _ = department_metadata.objects.get_or_create(
                dept_code=row['Department Code'],
                defaults={'dept_name': row['Department']}
            )

            # user_data,created = User.objects.get_or_create(email = row['Current Work Email'],first_name = first_name,
            #                                                last_name = last_name,username = )

            # Employee Handling Optimization
            employee_data_value, created = employee_metadata.objects.get_or_create(
            employee_id=emp_id,
            defaults={'first_name': first_name, 'last_name': last_name, 'job_title': title, 'dept': department_value}
            )

            # Handle ManyToManyField separately after object creation
            if created:
                employee_data_value.work_location.set([city])  # Use .set() for ManyToManyField
            else:
                employee_data_value.first_name = first_name
                employee_data_value.last_name = last_name
                employee_data_value.job_title = title
                employee_data_value.dept = department_value
                employee_data_value.save()  

                # Update work_location (ManyToManyField)
                employee_data_value.work_location.clear()  # Remove old locations
                employee_data_value.work_location.add(city)  # Add the new location


            # Supervisor Handling
            supervisor_data = row["Supervisor's Name (First Last)"].split(' ', 1)
            supervisor_data_first_name = supervisor_data[0]
            supervisor_data_last_name = supervisor_data[1] if len(supervisor_data) > 1 else ''

            supervisor_data_emp_id = row["Supervisor's Employee Code"]

            super_emp, _ = employee_metadata.objects.get_or_create(
                employee_id=supervisor_data_emp_id,
                defaults={'first_name': supervisor_data_first_name, 'last_name': supervisor_data_last_name}
            )

            # Supervisor Metadata Handling
            supervisor_metadata.objects.get_or_create(employee_data=employee_data_value, supervisor=super_emp)

        return JsonResponse({'message': True})




'''When someone click on next week button to see the how many employees are on leave next week '''
class next_week_function(TemplateView):


    def get(self, request, *args, **kwargs):
        data = request.GET
        next_week_date = data.get('next_date')
        last_week_date = datetime.datetime.strptime(next_week_date, "%B %d, %Y").date() - relativedelta(weeks=3)
        new_date = datetime.datetime.strptime(next_week_date, "%B %d, %Y").date() + datetime.timedelta(days=1)
        period = new_date + relativedelta(weeks=+3)

        data3 = []
        data4 = []
        data5 = []
        label = []

        delta = timedelta(days=1)
        period_leave = period
        start_date = new_date

        # Convert dates to timezone-aware datetime objects
        start_date = timezone.make_aware(datetime.datetime.combine(start_date, datetime.time.min))
        period_leave = timezone.make_aware(datetime.datetime.combine(period_leave, datetime.time.max))
        filters = Q()

        depart_list = data.getlist('depart[]')
        location_list = data.getlist('locat[]')
        # Apply location filter only if location_list has values
        if location_list:
            filters &= Q(work_location__name__in=location_list)

        # Apply department filter only if depart_list has values
        if depart_list:
            filters &= Q(dept_id__in=depart_list)

        if request.user.id in [1,2]:

            if depart_list or location_list:
                emp_dept = employee_metadata.objects.prefetch_related('work_location').select_related('dept').filter(filters).exclude(id__in = [579,704, 706, 582, 711, 585, 716, 718, 622, 688, 752, 633])
                total_emp_count = emp_dept.count()
            
            else:

                emp_dept = employee_metadata.objects.select_related().all().exclude(id__in = [579,704, 706, 582, 711, 585, 716, 718, 622, 688, 752, 633])
                total_emp_count = emp_dept.count()

            emp_data_id = list({emp.id for emp in emp_dept})
            # Get all holiday data as timezone-aware datetimes
            holidays = holiday_metadata.objects.filter(
                start_date__lte=period_leave, 
                end_date__gte=start_date
            )

            holiday_data = holidays.order_by('start_date') 
            leave_date = leave_metadata.objects.select_related('employee').filter(start_date__date__lte = period_leave,end_date__gte=start_date,employee_id__in = emp_data_id, request_status=True).order_by('-start_date')
            while start_date.date() <= period_leave.date():
                # Skip weekends
                if start_date.weekday() > 4:
                    start_date += delta
                    continue

                holiday_count = 0
                for emp in emp_dept:
                    if emp.work_location.all().exists():
                        # Convert to timezone-aware datetime before filtering
                        if holidays.filter(
                            country__name=emp.work_location.all()[0].name,
                            start_date__lte=start_date,
                            end_date__gte=start_date
                        ):
                            holiday_count += 1

                # Convert leave query to use timezone-aware datetime
                total_leave = leave_metadata.objects.filter(
                    start_date__date__lte=start_date.date(),
                    end_date__date__gte=start_date.date(),employee_id__in=emp_data_id,
                    request_status=True
                ).count()

                total = holiday_count + total_leave
                # data3.append(total_emp_count - total)  # Employee available
                # data4.append(total_leave)  # Employees on leave
                # data5.append(holiday_count)  # Employees on holiday

                data3.append(0 if holiday_count == total_emp_count else total_emp_count - total)  # Employee available
                data4.append(0 if holiday_count == total_emp_count else total_leave )  # Employees on leave
                data5.append(holiday_count)  # Employees on holiday

                label.append(f'{start_date.strftime("%m/%d/%Y")}')

                start_date += delta  # Move to the next day

            # Prepare JSON response
            data = {
                "labels": label,
                'data1': data3,
                'data2': data4,
                'data3': data5,
                'total_emp': total_emp_count
            }

            new_content1 = render_to_string('leave_table_replace.html', {'leave_data':leave_date})
            holiday_content = render_to_string('holiday_table_replace.html', {'holiday_data':holiday_data})
            return JsonResponse({
                'data': data,
                'next_week': period.strftime("%B %d, %Y"),
                'previous_week': last_week_date.strftime("%B %d, %Y"),
                'element1':new_content1,
                'holiday_content':holiday_content

            }, safe=False)
        
        elif request.user.id in [-22]:

            work_locations_id = list(employee_metadata.objects.filter(user_id=self.request.user.id).values_list('work_location__name', flat=True))
            if depart_list or location_list:
                emp_dept = employee_metadata.objects.prefetch_related('work_location').select_related('dept') \
                            .filter(filters).exclude(id__in=[579, 704, 706, 582, 711, 585, 716, 718, 622, 688, 752, 633])
            else:
                emp_dept = employee_metadata.objects.prefetch_related('work_location') \
                            .filter(work_location__name__in=work_locations_id) \
                            .exclude(id__in=[579, 704, 706, 582, 711, 585, 716, 718, 622, 688, 752, 633])

            total_emp_count = emp_dept.count()

            # Extract employee IDs
            emp_data_id = list(emp_dept.values_list('id', flat=True))

            # Optimized country_value extraction (Fixing the loop order issue)
            country_value = list({work_location.name for emp in emp_dept for work_location in emp.work_location.all()})

            # Get all holiday data as timezone-aware datetimes
            holidays = holiday_metadata.objects.select_related('country').filter(
                start_date__lte=period_leave, 
                end_date__gte=start_date,
                country__name__in = country_value
            )

            holiday_data = holidays.order_by('start_date') 
            leave_date = leave_metadata.objects.select_related('employee').filter(start_date__date__lte = period_leave,end_date__gte=start_date,employee_id__in = emp_data_id, request_status=True).order_by('-start_date')
            while start_date.date() <= period_leave.date():
                # Skip weekends
                if start_date.weekday() > 4:
                    start_date += delta
                    continue

                holiday_count = 0
                for emp in emp_dept:
                    if emp.work_location.all().exists():
                        # Convert to timezone-aware datetime before filtering
                        if holiday_metadata.objects.select_related('country').filter(
                            start_date__lte=start_date,
                            end_date__gte=start_date,country__name__in = country_value
                        ).exists():
                            holiday_count += 1


                        # Convert leave query to use timezone-aware datetime
                total_leave = leave_metadata.objects.filter(
                    start_date__date__lte=start_date.date(),
                    end_date__date__gte=start_date.date(),employee_id__in=emp_data_id,
                    request_status=True
                ).count()
        
                total = holiday_count + total_leave
                data3.append(0 if holiday_count == total_emp_count else total_emp_count - total)  # Employee available
                data4.append(0 if holiday_count == total_emp_count else total_leave )  # Employees on leave
                data5.append(holiday_count)  # Employees on holiday
                label.append(f'{start_date.strftime("%m/%d/%Y")}')

                start_date += delta  # Move to the next day

            # Prepare JSON response
            data = {
                "labels": label,
                'data1': data3,
                'data2': data4,
                'data3': data5,
                'total_emp': total_emp_count
            }

            new_content1 = render_to_string('leave_table_replace.html', {'leave_data':leave_date})
            holiday_content = render_to_string('holiday_table_replace.html', {'holiday_data':holiday_data})
            return JsonResponse({
                'data': data,
                'next_week': period.strftime("%B %d, %Y"),
                'previous_week': last_week_date.strftime("%B %d, %Y"),
                'element1':new_content1,
                'holiday_content':holiday_content

            }, safe=False)
        
        else:
            emp_list = indirect_supervisor(request)

            filters &=Q(id__in = emp_list)
            '''Below from pervious next functionality'''
            # work_locations_id = list(employee_metadata.objects.filter(user_id=self.request.user.id).values_list('work_location__name', flat=True))
            if depart_list or location_list:
                emp_dept = employee_metadata.objects.prefetch_related('work_location').select_related('dept') \
                            .filter(filters).exclude(
                                    Q(work_location=None) & Q(user_id__in=[522])
                                    
                                )
            else:
                emp_dept = employee_metadata.objects.prefetch_related('work_location').filter(
                                    id__in = emp_list
                                ).exclude(
                                    Q(work_location=None) & Q(user_id__in=[522])
                                    
                                )

            total_emp_count = emp_dept.count()

            # Extract employee IDs
            emp_data_id = list(emp_dept.values_list('id', flat=True))

            # Optimized country_value extraction (Fixing the loop order issue)
            country_value = list({work_location.name for emp in emp_dept for work_location in emp.work_location.all()})

            # Get all holiday data as timezone-aware datetimes
            holidays = holiday_metadata.objects.select_related('country').filter(
                start_date__lte=period_leave, 
                end_date__gte=start_date,
                country__name__in = country_value
            )

            holiday_data = holidays.order_by('start_date') 
            leave_date = leave_metadata.objects.select_related('employee').filter(start_date__date__lte = period_leave,end_date__gte=start_date,employee_id__in = emp_data_id, request_status=True).order_by('-start_date')
            while start_date.date() <= period_leave.date():
                # Skip weekends
                if start_date.weekday() > 4:
                    start_date += delta
                    continue

                holiday_count = 0
                for emp in emp_dept:
                    if emp.work_location.all().exists():
                        # Convert to timezone-aware datetime before filtering
                        if holiday_metadata.objects.select_related('country').filter(
                            start_date__lte=start_date,
                            end_date__gte=start_date,country__name__in = country_value
                        ).exists():
                            holiday_count += 1


                        # Convert leave query to use timezone-aware datetime
                total_leave = leave_metadata.objects.filter(
                    start_date__date__lte=start_date.date(),
                    end_date__date__gte=start_date.date(),employee_id__in=emp_data_id,
                    request_status=True
                ).count()
        
                total = holiday_count + total_leave
                data3.append(0 if holiday_count == total_emp_count else total_emp_count - total)  # Employee available
                data4.append(0 if holiday_count == total_emp_count else total_leave )  # Employees on leave
                data5.append(holiday_count)  # Employees on holiday
                label.append(f'{start_date.strftime("%m/%d/%Y")}')

                start_date += delta  # Move to the next day

            # Prepare JSON response
            data = {
                "labels": label,
                'data1': data3,
                'data2': data4,
                'data3': data5,
                'total_emp': total_emp_count
            }

            new_content1 = render_to_string('leave_table_replace.html', {'leave_data':leave_date})
            holiday_content = render_to_string('holiday_table_replace.html', {'holiday_data':holiday_data})
            return JsonResponse({
                'data': data,
                'next_week': period.strftime("%B %d, %Y"),
                'previous_week': last_week_date.strftime("%B %d, %Y"),
                'element1':new_content1,
                'holiday_content':holiday_content

            }, safe=False)
            








'''When someone click on previous week button to see the how many employees are on leave next week '''
class prev_week_function(TemplateView):


    def get(self, request, *args, **kwargs):
        data = request.GET
        next_week_date = data.get('next_date')
        previous_week_date = data.get('prev_date')
        last_week_date = datetime.datetime.strptime(previous_week_date, "%B %d, %Y").date()- datetime.timedelta(days=1) - relativedelta(weeks=3)
        new_date = datetime.datetime.strptime(previous_week_date, "%B %d, %Y").date()
        period = new_date + relativedelta(weeks=+3) #It return next 3 week date.

        data3 = []
        data4 = []
        data5 = []
        label = []

        delta = timedelta(days=1)
        period_leave = period
        start_date = new_date

        # Convert dates to timezone-aware datetime objects
        start_date = timezone.make_aware(datetime.datetime.combine(start_date, datetime.time.min))
        period_leave = timezone.make_aware(datetime.datetime.combine(period_leave, datetime.time.max))

        filters = Q()

        depart_list = data.getlist('depart[]')
        location_list = data.getlist('locat[]')
        # Apply location filter only if location_list has values
        if location_list:
            filters &= Q(work_location__name__in=location_list)

        # Apply department filter only if depart_list has values
        if depart_list:
            filters &= Q(dept_id__in=depart_list)

        if request.user.id in [1,2]:
            
            if filter:
                emp_dept = employee_metadata.objects.prefetch_related('work_location').select_related('dept').filter(filters).exclude(id__in = [579,704, 706, 582, 711, 585, 716, 718, 622, 688, 752, 633])
                total_emp_count = emp_dept.count()
            
            else:

                emp_dept = employee_metadata.objects.select_related().all().exclude(id__in = [579,704, 706, 582, 711, 585, 716, 718, 622, 688, 752, 633])
                total_emp_count = emp_dept.count()

            emp_data_id = list({emp.id for emp in emp_dept})

            # Get all holiday data as timezone-aware datetimes
            holidays = holiday_metadata.objects.filter(
                start_date__lte=period_leave, 
                end_date__gte=start_date
            )
            holiday_data = holidays.order_by('start_date') 
            leave_date = leave_metadata.objects.select_related('employee').filter(start_date__date__lte = period_leave,end_date__gte=start_date,employee_id__in = emp_data_id, request_status=True).order_by('-start_date')

            while start_date.date() <= period_leave.date():
                # Skip weekends
                if start_date.weekday() > 4:
                    start_date += delta
                    continue

                holiday_count = 0
                for emp in emp_dept:
                    if emp.work_location.all().exists():
                        # Convert to timezone-aware datetime before filtering
                        if holidays.filter(
                            country_id=emp.work_location.all()[0].id,
                            start_date__lte=start_date,
                            end_date__gte=start_date
                        ):
                            holiday_count += 1

                # Convert leave query to use timezone-aware datetime
                total_leave = leave_metadata.objects.filter(
                    start_date__date__lte=start_date.date(),
                    end_date__date__gte=start_date.date(),employee_id__in = emp_data_id,
                    request_status=True
                ).count()

                total = holiday_count + total_leave
                # data3.append(total_emp_count - total)  # Employee available
                # data4.append(total_leave)  # Employees on leave
                # data5.append(holiday_count)  # Employees on holiday
                data3.append(0 if holiday_count == total_emp_count else total_emp_count - total)  # Employee available
                data4.append(0 if holiday_count == total_emp_count else total_leave )  # Employees on leave
                data5.append(holiday_count)  # Employees on holiday
                label.append(f'{start_date.strftime("%m/%d/%Y")}')

                start_date += delta  # Move to the next day

            # Prepare JSON response
            data = {
                "labels": label,
                'data1': data3,
                'data2': data4,
                'data3': data5,
                'total_emp': total_emp_count
            }
            new_content1 = render_to_string('leave_table_replace.html', {'leave_data':leave_date})
            holiday_content = render_to_string('holiday_table_replace.html', {'holiday_data':holiday_data})
            return JsonResponse({
                'data': data,
                'next_week': period.strftime("%B %d, %Y"),
                'previous_week': last_week_date.strftime("%B %d, %Y"),
                'element1':new_content1,
                'holiday_content':holiday_content
            }, safe=False)
        
        elif request.user.id in [-22]:
            work_locations_id = list(employee_metadata.objects.filter(user_id=self.request.user.id).values_list('work_location__name', flat=True))
            if depart_list or location_list:
                emp_dept = employee_metadata.objects.prefetch_related('work_location').select_related('dept').filter(filters).exclude(id__in = [579,704, 706, 582, 711, 585, 716, 718, 622, 688, 752, 633])
                total_emp_count = emp_dept.count()
            
            else:

                emp_dept = employee_metadata.objects.prefetch_related('work_location').filter(work_location__name__in = work_locations_id).exclude(id__in = [579,704, 706, 582, 711, 585, 716, 718, 622, 688, 752, 633])
                total_emp_count = emp_dept.count()

            emp_data_id = list(emp_dept.values_list('id', flat=True))

            # Optimized country_value extraction (Fixing the loop order issue)
            country_value = list({work_location.name for emp in emp_dept for work_location in emp.work_location.all()})

            # Get all holiday data as timezone-aware datetimes
            holidays = holiday_metadata.objects.filter(
                start_date__lte=period_leave, 
                end_date__gte=start_date,
                country__name__in = country_value
            )

            # Get all holiday data as timezone-aware datetimes
            holiday_data = holidays.order_by('start_date') 
            leave_date = leave_metadata.objects.select_related('employee').filter(start_date__date__lte = period_leave,end_date__gte=start_date,employee_id__in = emp_data_id, request_status=True).order_by('-start_date')

            while start_date.date() <= period_leave.date():
                # Skip weekends
                if start_date.weekday() > 4:
                    start_date += delta
                    continue

                holiday_count = 0
                for emp in emp_dept:
                    if emp.work_location.all().exists():
                        # Convert to timezone-aware datetime before filtering
                        if holidays.filter(
                            start_date__lte=start_date,
                            end_date__gte=start_date
                        ):
                            holiday_count += 1

                # Convert leave query to use timezone-aware datetime
                total_leave = leave_metadata.objects.filter(
                    start_date__date__lte=start_date.date(),
                    end_date__date__gte=start_date.date(),employee_id__in=emp_data_id,
                    request_status=True
                ).count()

                total = holiday_count + total_leave
                # data3.append(total_emp_count - total)  # Employee available
                # data4.append(total_leave)  # Employees on leave
                # data5.append(holiday_count)  # Employees on holiday
                data3.append(0 if holiday_count == total_emp_count else total_emp_count - total)  # Employee available
                data4.append(0 if holiday_count == total_emp_count else total_leave )  # Employees on leave
                data5.append(holiday_count)  # Employees on holiday
                label.append(f'{start_date.strftime("%m/%d/%Y")}')

                start_date += delta  # Move to the next day

            # Prepare JSON response
            data = {
                "labels": label,
                'data1': data3,
                'data2': data4,
                'data3': data5,
                'total_emp': total_emp_count
            }
            new_content1 = render_to_string('leave_table_replace.html', {'leave_data':leave_date})
            holiday_content = render_to_string('holiday_table_replace.html', {'holiday_data':holiday_data})
            return JsonResponse({
                'data': data,
                'next_week': period.strftime("%B %d, %Y"),
                'previous_week': last_week_date.strftime("%B %d, %Y"),
                'element1':new_content1,
                'holiday_content':holiday_content
            }, safe=False)
        
        else:
            emp_list = indirect_supervisor(request)
            

            filters &=Q(id__in = emp_list)
            '''Below from pervious next functionality'''
            if depart_list or location_list:
                emp_dept = employee_metadata.objects.prefetch_related('work_location').select_related('dept').filter(filters).exclude(
                                    Q(work_location=None) & Q(user_id__in=[522])
                                    
                                )
                total_emp_count = emp_dept.count()
            
            else:

                emp_dept = employee_metadata.objects.prefetch_related('work_location').filter(
                                    id__in = emp_list
                                ).exclude(
                                    Q(work_location=None) & Q(user_id__in=[522])
                                    
                                )
                total_emp_count = emp_dept.count()

            emp_data_id = list(emp_dept.values_list('id', flat=True))

            # Optimized country_value extraction (Fixing the loop order issue)
            country_value = list({work_location.name for emp in emp_dept for work_location in emp.work_location.all()})

            # Get all holiday data as timezone-aware datetimes
            holidays = holiday_metadata.objects.filter(
                start_date__lte=period_leave, 
                end_date__gte=start_date,
                country__name__in = country_value
            )

            # Get all holiday data as timezone-aware datetimes
            holiday_data = holidays.order_by('start_date') 
            leave_date = leave_metadata.objects.select_related('employee').filter(start_date__date__lte = period_leave,end_date__gte=start_date,employee_id__in = emp_data_id, request_status=True).order_by('-start_date')

            while start_date.date() <= period_leave.date():
                # Skip weekends
                if start_date.weekday() > 4:
                    start_date += delta
                    continue

                holiday_count = 0
                for emp in emp_dept:
                    if emp.work_location.all().exists():
                        # Convert to timezone-aware datetime before filtering
                        if holidays.filter(
                            start_date__lte=start_date,
                            end_date__gte=start_date
                        ):
                            holiday_count += 1

                # Convert leave query to use timezone-aware datetime
                total_leave = leave_metadata.objects.filter(
                    start_date__date__lte=start_date.date(),
                    end_date__date__gte=start_date.date(),employee_id__in=emp_data_id,
                    request_status=True
                ).count()

                total = holiday_count + total_leave
                # data3.append(total_emp_count - total)  # Employee available
                # data4.append(total_leave)  # Employees on leave
                # data5.append(holiday_count)  # Employees on holiday
                data3.append(0 if holiday_count == total_emp_count else total_emp_count - total)  # Employee available
                data4.append(0 if holiday_count == total_emp_count else total_leave )  # Employees on leave
                data5.append(holiday_count)  # Employees on holiday
                label.append(f'{start_date.strftime("%m/%d/%Y")}')

                start_date += delta  # Move to the next day

            # Prepare JSON response
            data = {
                "labels": label,
                'data1': data3,
                'data2': data4,
                'data3': data5,
                'total_emp': total_emp_count
            }
            new_content1 = render_to_string('leave_table_replace.html', {'leave_data':leave_date})
            holiday_content = render_to_string('holiday_table_replace.html', {'holiday_data':holiday_data})
            return JsonResponse({
                'data': data,
                'next_week': period.strftime("%B %d, %Y"),
                'previous_week': last_week_date.strftime("%B %d, %Y"),
                'element1':new_content1,
                'holiday_content':holiday_content
            }, safe=False)  
        

            
        




class filterhome(TemplateView):
    def post(self,request,*args,**kwargs):

        if request.user.id in [1,2]:
            depart_list = request.POST.getlist('department-select')
            location_list = request.POST.getlist('location-select')
            previous_week_date = request.POST.get('next_date')
            if previous_week_date:
                last_week_date = datetime.datetime.strptime(previous_week_date, "%B %d, %Y").date() - relativedelta(weeks=3)
                period = last_week_date + relativedelta(weeks=+3) #It return next 3 week date.
                print(last_week_date)

            
            filters = Q()

            # Apply location filter only if location_list has values
            if location_list:
                filters &= Q(work_location__name__in=location_list)

            # Apply department filter only if depart_list has values
            if depart_list:
                filters &= Q(dept_id__in=depart_list)

            # Apply the filters to the query
            emp_data = employee_metadata.objects.prefetch_related('work_location').select_related('dept').filter(filters)

            emp_data_id = list({emp.id for emp in emp_data})

            # next_week_date = data.get('next_date')

            # last_week_date = datetime.datetime.strptime(next_week_date, "%B %d, %Y").date() - relativedelta(weeks=3)
            
            data3 = []
            data4 = []
            data5 = []
            label = []

            delta = timedelta(days=1)
            period_leave = period
            start_date = last_week_date

            # Convert dates to timezone-aware datetime objects
            start_date = timezone.make_aware(datetime.datetime.combine(start_date, datetime.time.min))
            period_leave = timezone.make_aware(datetime.datetime.combine(period_leave, datetime.time.max))


            emp_dept = emp_data
            total_emp_count = emp_dept.count()

            # Get all holiday data as timezone-aware datetimes
            holidays = holiday_metadata.objects.select_related().filter(
                start_date__lte=period_leave, 
                end_date__gte=start_date
            )

            '''Filter Depending upon employee..'''
            leave_date = leave_metadata.objects.select_related('employee').filter(start_date__date__lte = period_leave,end_date__gte=start_date,request_status=True,
                                                                                employee_id__in = emp_data_id).order_by('-start_date')
            while start_date.date() <= period_leave.date():
                # Skip weekends
                if start_date.weekday() > 4:
                    start_date += delta
                    continue

                holiday_count = 0
                for emp in emp_dept:
                    if emp.work_location.all().exists():
                        # Convert to timezone-aware datetime before filtering
                        if holidays.filter(
                            country__name=emp.work_location.all()[0].name,
                            start_date__lte=start_date,
                            end_date__gte=start_date
                        ):
                            holiday_count += 1

                # Convert leave query to use timezone-aware datetime
                total_leave = leave_metadata.objects.filter(
                    start_date__date__lte=start_date.date(),
                    end_date__date__gte=start_date.date(),employee_id__in = emp_data_id,
                    request_status=True
                ).count()

                total = holiday_count + total_leave
                
                data3.append(0 if holiday_count == total_emp_count else total_emp_count - total)  # Employee available
                data4.append(0 if holiday_count == total_emp_count else total_leave )  # Employees on leave
                data5.append(holiday_count)  # Employees on holiday
                label.append(f'{start_date.strftime("%m/%d/%Y")}')

                start_date += delta  # Move to the next day

            # Prepare JSON response
            data = {
                "labels": label,
                'data1': data3,
                'data2': data4,
                'data3': data5,
                'total_emp': total_emp_count
            }
            new_content1 = render_to_string('leave_table_replace.html', {'leave_data':leave_date})
            return JsonResponse({
                'data': data,
                'element1':new_content1
                # 'next_week': period.strftime("%B %d, %Y"),
                # 'previous_week': last_week_date.strftime("%B %d, %Y")

            }, safe=False)
        
        else:
            emp_list_get = indirect_supervisor(request)


            depart_list = request.POST.getlist('department-select')
            location_list = request.POST.getlist('location-select')
            previous_week_date = request.POST.get('next_date')
            if previous_week_date:
                last_week_date = datetime.datetime.strptime(previous_week_date, "%B %d, %Y").date() - relativedelta(weeks=3)
                period = last_week_date + relativedelta(weeks=+3) #It return next 3 week date.
                print(last_week_date)

            
            filters = Q()

            # Apply location filter only if location_list has values
            if location_list:
                filters &= Q(work_location__name__in=location_list)

            # Apply department filter only if depart_list has values
            if depart_list:
                filters &= Q(dept_id__in=depart_list)

            filters &=Q(id__in = emp_list_get)
            # Apply the filters to the query
            emp_data = employee_metadata.objects.prefetch_related('work_location').select_related('dept').filter(filters)

            emp_data_id = list({emp.id for emp in emp_data})

            # next_week_date = data.get('next_date')

            # last_week_date = datetime.datetime.strptime(next_week_date, "%B %d, %Y").date() - relativedelta(weeks=3)
            
            data3 = []
            data4 = []
            data5 = []
            label = []

            delta = timedelta(days=1)
            period_leave = period
            start_date = last_week_date

            # Convert dates to timezone-aware datetime objects
            start_date = timezone.make_aware(datetime.datetime.combine(start_date, datetime.time.min))
            period_leave = timezone.make_aware(datetime.datetime.combine(period_leave, datetime.time.max))


            emp_dept = emp_data
            total_emp_count = emp_dept.count()

            # Get all holiday data as timezone-aware datetimes
            holidays = holiday_metadata.objects.select_related().filter(
                start_date__lte=period_leave, 
                end_date__gte=start_date
            )

            '''Filter Depending upon employee..'''
            leave_date = leave_metadata.objects.select_related('employee').filter(start_date__date__lte = period_leave,end_date__gte=start_date,request_status=True,
                                                                                employee_id__in = emp_data_id).order_by('-start_date')
            while start_date.date() <= period_leave.date():
                # Skip weekends
                if start_date.weekday() > 4:
                    start_date += delta
                    continue

                holiday_count = 0
                for emp in emp_dept:
                    if emp.work_location.all().exists():
                        # Convert to timezone-aware datetime before filtering
                        if holidays.filter(
                            country__name=emp.work_location.all()[0].name,
                            start_date__lte=start_date,
                            end_date__gte=start_date
                        ):
                            holiday_count += 1

                print(f'holiday count {holiday_count}')
                # Convert leave query to use timezone-aware datetime
                total_leave = leave_metadata.objects.filter(
                    start_date__date__lte=start_date.date(),
                    end_date__date__gte=start_date.date(),employee_id__in = emp_data_id,
                    request_status=True
                ).count()

                total = holiday_count + total_leave
                # data3.append(total_emp_count - total)  # Employee available
                # data4.append(total_leave)  # Employees on leave
                # data5.append(holiday_count)  # Employees on holiday
                data3.append(0 if holiday_count == total_emp_count else total_emp_count - total)  # Employee available
                data4.append(0 if holiday_count == total_emp_count else total_leave )  # Employees on leave
                data5.append(holiday_count)  # Employees on holiday
                label.append(f'{start_date.strftime("%m/%d/%Y")}')

                start_date += delta  # Move to the next day

            # Prepare JSON response
            data = {
                "labels": label,
                'data1': data3,
                'data2': data4,
                'data3': data5,
                'total_emp': total_emp_count
            }
            new_content1 = render_to_string('leave_table_replace.html', {'leave_data':leave_date})
            return JsonResponse({
                'data': data,
                'element1':new_content1
                # 'next_week': period.strftime("%B %d, %Y"),
                # 'previous_week': last_week_date.strftime("%B %d, %Y")

            }, safe=False)

    



class clear_filter_home(TemplateView):
    template_name = ''

    def get(self,request,*args,**kwargs):

        if request.user.id in [1,2]:
            context = {}

            # Optimized Query for Supervisors


            # Optimized Query for Departments
            dept_data = department_metadata.objects.all().order_by('dept_name')

            # Optimized Work Location Deduplication
            country_value = sorted(
                    set(
                        work_name
                        for emp in employee_metadata.objects.prefetch_related('work_location')
                        .exclude(id__in=[579])
                        for work_name in emp.work_location.values_list('name', flat=True)
                    )
                )

            context['dept_data'] = dept_data
            context['work_location'] = country_value
            new_content1 = render_to_string('clear_filter_home.html', context)
            return JsonResponse({'message':True,'element':new_content1})
        
        else:

            emp_list_get = indirect_supervisor(request)
            super_emp = employee_metadata.objects.filter(id__in = emp_list_get)
            dept_data = department_metadata.objects.filter(id__in = list({i.dept.id for i in super_emp}))
            context = {}


            country_value = sorted(
                    set(
                        work_name
                        for emp in employee_metadata.objects.filter(id__in=list({i.id for i in super_emp})).exclude(Q(work_location=None) & Q(user_id__in=[522]))
                        for work_name in emp.work_location.values_list('name', flat=True)
                    )
                )
            
            

            context['dept_data'] = dept_data
            context['work_location'] = country_value
            new_content1 = render_to_string('clear_filter_home.html', context)
            return JsonResponse({'message':True,'element':new_content1})


# print(Mailer().change_toaddrs(['khan@gmail.com']))
class email_cron_function(TemplateView):

    def get(self,request,*args,**kwargs):
        email_model_obj = email_model.objects.select_related('leave_employee').filter(email_send = False)

        for obj in email_model_obj:
            toaddrs_lst = obj.email_send_to
            print(toaddrs_lst)
            email = Mailer()
            email.change_toaddrs(toaddrs_lst)
            email.change_subject(f'Notification | Employee on leave | {obj.leave_employee.employee.first_name} {obj.leave_employee.employee.last_name}')

            try:
                body = email.run_method(obj)
                obj.email_send = True
                obj.email_body = body
                obj.save()

            except Exception as e:
                obj.email_error = str(e)  # Convert Exception to string

        
        return HttpResponse('Email Run Successfull!!')
    


class TestEmail(TemplateView):
    def get(self,request,*args,**kwargs):
        
        context = {}
        email_model_ob = email_model.objects.all()[0]
        context['obj'] = email_model_ob
        return render(request,'email_notification.html',context)
    




import pandas as pd
from django.views.generic import TemplateView

class ExportDetail(TemplateView):
    def get(self, request, *args, **kwargs):
        supervisor_data = supervisor_metadata.objects.select_related().all()

        data_list = []

        for data in supervisor_data:
            employee = data.employee_data
            supervisor = data.supervisor

            data_dict = {
                'Employee Id': employee.employee_id,
                'Last Name': employee.last_name,
                'Preferred/First Name': employee.first_name,
                'Department Code': employee.dept.dept_code,
                'Department': employee.dept.dept_name,
                'Work Email': employee.work_email if employee.work_email else '',
                'Work Location Name': ' '.join([i.name for i in employee.work_location.all()]) if employee.work_location else '',
                'Job Title': employee.job_title if employee.job_title else '',
                "Supervisor's Employee ID": supervisor.employee_id,
                "Supervisor's Name (First Last)": f'{supervisor.first_name} {supervisor.last_name}',
                "Supervisor's Work Email": supervisor.work_email if supervisor.work_email else '',
                "Indirect Supervisor's Name (First Last)": "",
                "Indirect Supervisor's Work Email": "",
                "Indirect Supervisor's Employee ID": ""
            }

            data_list.append(data_dict)

        df = pd.DataFrame(data_list)

        # print(df)

        df.to_excel('Employees Comprehensive Demographic List.xlsx', index=False)

        return HttpResponse("Export complete")
    



class FilterFormSubmit(TemplateView):

    def post(self,request,*args,**kwargs):


        print(request.POST)

        return HttpResponse('GOT IT')




            
