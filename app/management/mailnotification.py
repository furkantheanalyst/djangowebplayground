from django.conf import settings
from django.core.mail import EmailMessage, get_connection

def send_email(useremail, verification_code):  
    with get_connection(  
     host=settings.EMAIL_HOST, 
     port=settings.EMAIL_PORT,  
     username=settings.EMAIL_HOST_USER, 
     password=settings.EMAIL_HOST_PASSWORD, 
     use_tls=settings.EMAIL_USE_TLS  
       ) as connection:  
           subject = "Login Verification Code" 
           from_email = settings.EMAIL_HOST_USER  
           recipient_list = [useremail]
           message = ("New Login Detected from Istanbul, Turkey, Verification Code: "+ verification_code)  
           EmailMessage(subject, message, from_email, recipient_list, connection=connection).send()  
 
