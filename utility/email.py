import smtplib
from email.mime.multipart import MIMEMultipart
from django.core.mail import EmailMultiAlternatives
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
from email.mime.base import MIMEBase
from email import encoders
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.utils.html import strip_tags
from email.mime.text import MIMEText

class Mailer:
    def __init__(self):
      
        self.toaddrs = ['sameer.saurabh@escalent.co','deepak.singh@escalent.co','imran.khan@escalent.co']
        self.fromaddr = 'notifications@escalent.co'
        self.message_subject = "Test Email"
        self.server = smtplib.SMTP('email.escalent.co', 25)
        
    def run(self,obj):
        
        message = self.create_message(obj)
        self.send_email(message)       
 
    def create_message(self,obj):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.message_subject
        msg['From'] = self.fromaddr
        # msg['To'] = ", ".join(self.toaddrs)
        html_content = render_to_string('email_notification.html', {'obj':obj}).strip()
        text_content = strip_tags(html_content)

        body =html_content
        part = MIMEText(body, 'html')

        msg.attach(part)

 
        return msg
    
    def send_email(self,message):
        self.server.sendmail(self.fromaddr, self.toaddrs, message.as_string())
        self.server.quit()

    def change_toaddrs(self,to=[]):

        if len(to)>0:
            # self.toaddrs = to
            self.toaddrs = ['Imran.Khan2@escalent.co','kwong@cspace.com','csippitt@cspace.com']
        return self.toaddrs
    
    def run_method(self,obj):
        # web = Mailer()
        self.run(obj)

    def change_subject(self,subject):
        self.message_subject = subject

        return self.message_subject