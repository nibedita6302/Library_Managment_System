import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders 
from email.mime.multipart import MIMEMultipart

from .createPDF import create_pdf
from application.models.users import Users 
from .credentials import get_email_credential

def sendEmail(user_id, email_type='reminder', message=None):
    ## Email account details
    sender_email, app_password = get_email_credential()
    user = Users.query.get(user_id)     ## Get recievers details

    ## Set up the email details
    if email_type=='reminder':  
        subject = "Library Reminder"
        body = f'''
        Dear {user.name}, 
        We see that you have not visited the Dgital Library today.
        Please visit and have a look at you favourite books and authors under MyBooks.

        Thank you
        Warm Regards 
        Librarian
        '''
    elif email_type=='info' and message is not None:
        print('in info')
        subject = "Library Book Issue Status"
        body = f'''
        Dear {user.name}, 
        This email is to inform you about your book status as follows:
        {message}

        Thank you
        Warm Regards 
        Librarian
        '''
    elif email_type=='info' and message is None:
        print('exception info')
        raise TypeError('Cannot send Email of email_type "info" with None message')
    else:
        month = datetime.now().strftime('%B')
        subject = f"Digital Library - Monthly User Activity Report - {month}"
        body = f'''
        The wait is over! 
        Your Monthly activity report for {month} is at last here. Check it out Now!

        Warm Regards
        Librarian
        '''
    message = MIMEMultipart()                   ## Create the MIME object
    message["From"] = sender_email
    message["To"] = user.email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))     ## Attach the body to the email

    if email_type=='report':                 
        file_path = create_pdf(user_id)                    ## Generate PDF   
        attachment = open(file_path, "rb")    ## open the file to be sent 
        
        p = MIMEBase('application', 'octet-stream')     ## instance of MIMEBase and named as p  
        p.set_payload((attachment).read())              ## To change the payload into encoded form
        encoders.encode_base64(p)                       ## encode into base64 
        filename = file_path.split('/')[-1]
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)  
        message.attach(p)                               ## attach the instance 'p' to instance 'msg'

    ## Establish a connection to the SMTP server (in this case, Gmail's SMTP server)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()                            ## Start the TLS (Transport Layer Security) mode
        server.login(sender_email, app_password)     ## Login to the email account using the App Password
        server.sendmail(sender_email, user.email, message.as_string())  ## Send the email