
from django.urls import path
# from . views import *
from . views import (base_view,login,calendar_view,calendar_function,new_calender_view,admin_view,resetpasswordview,
                        file_upload_view,test,home_view,chart_view_function,holiday_upload,project_detail_post,project_detail_fetch_function,
                        new_exisiting_project,add_project_view,add_exiting_project_view,update_calendar,
                        update_calendar_js,supervisor_select1,emp_select_function1,title_select_function1,project_select_function1,
                        dept_select_function,location_select_function,holiday_add,logout_function,
                        clear_filter_function,email_detail_post,supervisor_detail_post,outlook_calendar_download,
                        bluk_project_upload,employee_file_upload,next_week_function,prev_week_function,filterhome,
                        clear_filter_home,email_cron_function,TestEmail,ExportDetail,FilterFormSubmit
                    )

urlpatterns = [
    path('base/', base_view,name='base'),
    path('login/',login,name='login'),
    path('calendar/',calendar_view.as_view(),name='calendar'),
    path('calendarfunction/',calendar_function,name='calendar-function'),
    path('nwcalendar/',new_calender_view,name='nwcalendar'),
    path('profile/',admin_view.as_view(),name='profile'),
    path('passwordreset/',resetpasswordview.as_view(),name='password-reset'),
    # path('fileupload/',fiel_upload_view,name='file-upload'),
    path('fileupload/',file_upload_view.as_view(),name='file-upload'),
    path('testing/',test,name='testing'),
    path('',home_view.as_view(),name='home-page'),
    path('charts/',chart_view_function,name='chart'),
    path('chartfunction/',chart_view_function,name='chart-function'),
    path('holidayupload/',holiday_upload.as_view(),name='holiday-function'),
    path('project_detail/',project_detail_post.as_view(),name='project-detail-post'),
    path('projectdetailfetch/',project_detail_fetch_function.as_view(),name='project-detail-fetch'),
    path('changeproject/',new_exisiting_project.as_view(),name='change-project'),
    path('addproject/',add_project_view.as_view(),name='add-project'),
    path('existingprojectupdate/',add_exiting_project_view.as_view(),name='existing-project-update'),
    path('updatecalendar/',update_calendar.as_view(),name='update-calendar'),
    path('updatecalendarjs/<date>/<emp>/',update_calendar_js.as_view(),name='update-calendar-js'),
    path('supervisorselect/',supervisor_select1.as_view(),name='supervisor-select'),
    path('employeeselect/',emp_select_function1.as_view(),name='employee-select'),
    path('titleselect/',title_select_function1.as_view(),name='title-select'),
    path('projectselect/',project_select_function1.as_view(),name='project-select'),
    path('departmentselect/',dept_select_function.as_view(),name='dept-select'),
    path('locationselect/',location_select_function.as_view(),name='location-select'),
    path('holidayadd/',holiday_add.as_view(),name='holiday-add'),
    path('logout/',logout_function.as_view(),name='logouts'),
    path('clearfilter/',clear_filter_function.as_view(),name='clear-filter'),
    path('employee_add/',email_detail_post.as_view(),name='employee-add'),
    path('sup_add/',supervisor_detail_post.as_view(),name='sup-add'),
    path('outlookcalendar/',outlook_calendar_download.as_view(),name='outlook-calendar'),
    path('blukprojectupload/',bluk_project_upload.as_view(),name='bluk-project'),
    path('employee_upload/',employee_file_upload.as_view(),name='employee-upload'),
    path('nextweek/',next_week_function.as_view(),name='next-week-function'),#Next Week functionality url
    path('previousweek/',prev_week_function.as_view(),name='prev-week-function'),#Next Week functionality url
    path('homefilter/',filterhome.as_view(),name='home-filter'),#Next Week functionality url
    path('clearhomefilter/',clear_filter_home.as_view(),name='clear-home-filter'),#Next Week functionality url
    path('emailcrons/',email_cron_function.as_view(),name='email-cron'),
    path('testemail/',TestEmail.as_view(),name='test-email'),
    path('exportexcel/',ExportDetail.as_view(),name='export-excel'),
    path('filterformsubmit/',FilterFormSubmit.as_view(),name='filter-form-submit'),
    





]