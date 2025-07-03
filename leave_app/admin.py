from django.contrib import admin

from . models import (country_metadata,holiday_metadata,department_metadata,employee_metadata,indirectsupervisor_metadata,
                                             supervisor_metadata,leave_metadata,uploadleave_metadata,project_detail_model,
                                             project_detail,department_head_model,email_model)
from django.contrib.admin import ModelAdmin
# Register your models here.


@admin.register(country_metadata)
class country_metadata_admin(admin.ModelAdmin):
     list_display = ('id','name','city')




@admin.register(holiday_metadata)
class holiday_metadata_admin(admin.ModelAdmin):
     list_display = ('id','country','holiday_name','start_date','end_date','year')



@admin.register(department_metadata)
class department_metadata_admin(admin.ModelAdmin):
     list_display = ('id','dept_code','dept_name','dept_description')




class EmployeeMetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee_id','first_name','last_name', 'work_email','job_title','dept', 'get_work_locations')

    def get_work_locations(self, obj):
        return ", ".join([str(location) for location in obj.work_location.all()])

    get_work_locations.short_description = "Work Locations"  # Column name in the admin panel
    search_fields = ['id','employee_id']

admin.site.register(employee_metadata, EmployeeMetadataAdmin)



@admin.register(indirectsupervisor_metadata)
class indirectsupervisor_metadata_admin(admin.ModelAdmin):
     list_display = ('id','employee')


@admin.register(supervisor_metadata)
class supervisor_metadata_admin(admin.ModelAdmin):
     list_display = ('id','indirect_supervisor_metadata','supervisor','employee_data')


@admin.register(leave_metadata)
class leave_metadata_admin(admin.ModelAdmin):
     list_display = ('id','employee','start_date','end_date','hours','request_status')
     search_fields = ['id']



@admin.register(uploadleave_metadata)
class uploadleave_metadata_admin(admin.ModelAdmin):
     list_display = ('id','excel_file','upload_date')


@admin.register(project_detail_model)
class project_detail_model_admin(admin.ModelAdmin):
     list_display = ('id','project_name')

@admin.register(project_detail)
class project_detail_admin(admin.ModelAdmin):
     list_display = ('id','employee','project_name')


@admin.register(department_head_model)
class department_head_model_admin(admin.ModelAdmin):
     list_display = ('id','user','get_department_value')
     search_fields = ['department']

     def get_department_value(self, obj):
        return ", ".join([str(depart) for depart in obj.department.all()])


@admin.register(email_model)
class email_model_admin(admin.ModelAdmin):
     list_display = ('id','department_head','leave_employee','email_send_to','email_send',)
     search_fields = ['department_head']



