from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


'''Base Model which used create predefinedcolumn in each table..'''
class base_model(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    upload_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        abstract=True




'''This model used to store information about county'''
class country_metadata(base_model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        verbose_name= "Country MetaData"
        verbose_name_plural = "Country MetaData"

    def __str__(self):
        return self.name
    


'''Holiday Table for each county'''
class holiday_metadata(base_model):
    country = models.ForeignKey(country_metadata,on_delete=models.CASCADE)
    holiday_name = models.CharField(max_length=100)
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    pto_days = models.CharField(max_length=100,blank=True,null=True)
    year = models.IntegerField()


    class Meta:
        verbose_name= "Holiday Metadata"
        verbose_name_plural = "Holiday Metadata"

    def __str__(self):
        return self.holiday_name
    



'''Department MetaData having the record of department'''
class department_metadata(base_model):
    dept_code = models.CharField(max_length=100)
    dept_name = models.CharField(max_length=100)
    dept_description = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        verbose_name= "Department Metadata"
        verbose_name_plural = "Department Metadata"

    def __str__(self):
        return self.dept_name





'''EMPLOYEE METADATA HAVING RECORD OF EACH EMPLOYEE'''
class employee_metadata(base_model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    employee_id = models.CharField(max_length=100,null=True,blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    work_location = models.ManyToManyField(country_metadata,blank=True)
    work_email = models.EmailField(null=True,blank=True)
    job_title = models.CharField(max_length=100,null=True,blank=True)
    dept = models.ForeignKey(department_metadata,on_delete=models.CASCADE,null=True,blank=True)


    class Meta:
        verbose_name= "Employee Metadata"
        verbose_name_plural = "Employee Metadata"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



    


'''This table having the record of indrect supervisor level data '''
class indirectsupervisor_metadata(base_model):
    employee  = models.ForeignKey(employee_metadata,on_delete=models.CASCADE,null=True,blank=True)



    class Meta:
        verbose_name= "Indirectsupervisor Metadata"
        verbose_name_plural = "Indirectsupervisor Metadata"


    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name}'



class supervisor_metadata(base_model):
    indirect_supervisor_metadata = models.ForeignKey(indirectsupervisor_metadata,on_delete=models.CASCADE,null=True,blank=True)
    supervisor = models.ForeignKey(employee_metadata,on_delete=models.CASCADE,related_name='supervisor',null=True,blank=True)
    employee_data = models.ForeignKey(employee_metadata,models.CASCADE,related_name='employee_data')


    class Meta:
        verbose_name= "Supervisor Metadata"
        verbose_name_plural = "Supervisor Metadata"

    def __str__(self):

        return f'{self.employee_data.first_name} {self.employee_data.last_name}'
    


class uploadleave_metadata(base_model):
    excel_file = models.FileField(upload_to='excel_folder',null=True,blank=True)
    upload_date = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name= "UploadLeave Metadata"
        verbose_name_plural = "UploadLeave Metadata"

    def __str__(self):

        return f'{self.id}'
    




class leave_metadata(base_model):
    employee = models.ForeignKey(employee_metadata,on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    hours = models.IntegerField()
    request_status = models.BooleanField(default=False)
    upload_file = models.ForeignKey(uploadleave_metadata,on_delete=models.CASCADE,null=True,blank=True)


    class Meta:
        verbose_name= "Leave Metadata"
        verbose_name_plural = "Leave Metadata"

    def __str__(self):

        return f'{self.employee.first_name} {self.employee.last_name}'


class project_detail_model(base_model):
    project_name = models.CharField(max_length=100)

    class Meta:
        verbose_name= "Project Detail Model"
        verbose_name_plural = "Project Detail Model"

    def __str__(self):

        return f'{self.project_name}'


class project_detail(base_model):
    employee = models.ForeignKey(employee_metadata,on_delete=models.CASCADE)
    project_name = models.ForeignKey(project_detail_model,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        verbose_name= "Project Detail"
        verbose_name_plural = "Project Detail"

    def __str__(self):

        return f'{self.project_name}'
    


'''Department Head Tag Model'''
class department_head_model(base_model):
    user  = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    department = models.ManyToManyField(department_metadata,blank=True)

    class Meta:
        verbose_name= "Department Head Model"
        verbose_name_plural = "Department Head Model"

    def __str__(self):

        return f'{self.user}{self.department}'

'''Email Automation Model'''
class email_model(base_model):
    department_head = models.ForeignKey(department_head_model,on_delete=models.CASCADE,null=True,blank=True)
    leave_employee = models.ForeignKey(leave_metadata,on_delete=models.CASCADE)
    email_send_to = models.TextField()
    subject = models.CharField(max_length=150)
    email_body = models.TextField(null=True,blank=True)
    remainder = models.IntegerField(default=0)
    email_send = models.BooleanField(default=False)
    email_error = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name= "Email Model"
        verbose_name_plural = "Email Model"

    def __str__(self):

        return f'{self.department_head}'


