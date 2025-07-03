from . models import (email_model)
'''Email Model Import'''
from utility.email import Mailer


def email_notification():
    email_model_obj = email_model.objects.select_related('leave_employee').filter(email_send = False)

    for obj in email_model_obj:
        toaddrs_lst = obj.email_send_to
        print(toaddrs_lst)
        email = Mailer()
        toaddrs_lst = ['imran.khan1@escalent.co']
        email.change_toaddrs(toaddrs_lst)
        email.change_subject(f'Notification | Employee on leave | {obj.leave_employee.employee.first_name} {obj.leave_employee.employee.last_name}')

        try:
            body = email.run_method(obj)
            obj.email_send = True
            obj.email_body = body
            obj.save()

        except Exception as e:
            obj.email_error = str(e)  # Convert Exception to string