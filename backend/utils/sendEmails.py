import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders 
from email.mime.multipart import MIMEMultipart
from .createPDF import create_pdf

from application.models.users import Users
from .credentials import get_email_credential

def sendEmail(user_id, email_type='reminder'):
    ## Email account details
    sender_email, app_password = get_email_credential()
    user = Users.query.get(user_id)     ## Get recievers details

    ## Set up the email details
    if email_type=='reminder':  
        subject = "Library Reminder"
        body = f'''Dear {user.name}, 
        We see that you have not visited the Online Library.
        Please visit and have a look at you favourite books and authors under MyBooks.

        Thank you
        Regards 
        Librarian
        '''
    else:
        subject = "Monthly Activity Report - Online Library"
        body = '''The wait is over! 
        Your Monthly activity report is atlast here. Check it out Now!
        Regards
        Librarian
        '''
    message = MIMEMultipart()                   ## Create the MIME object
    message["From"] = sender_email
    message["To"] = user.email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))     ## Attach the body to the email

    if email_type=='report':                  
        month = datetime.now().strftime('%B')
        filename = f"{month}.pdf"
        create_pdf(filename, user_id)                    ## Generate PDF   
        attachment = open(f"./static/pdfs/{filename}", "rb")    ## open the file to be sent 
        
        p = MIMEBase('application', 'octet-stream')     ## instance of MIMEBase and named as p  
        p.set_payload((attachment).read())              ## To change the payload into encoded form
        encoders.encode_base64(p)                       ## encode into base64 
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)  
        message.attach(p)                               ## attach the instance 'p' to instance 'msg'

    ## Establish a connection to the SMTP server (in this case, Gmail's SMTP server)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()                            ## Start the TLS (Transport Layer Security) mode
        server.login(sender_email, app_password)     ## Login to the email account using the App Password
        server.sendmail(sender_email, user.email, message.as_string())  ## Send the email