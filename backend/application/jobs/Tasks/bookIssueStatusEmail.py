from application.models.books import Books
from application.jobs.workers import celery
from utils.sendEmails import sendEmail

@celery.task()
def revoke_issue_email(user_id, book_id):
    book_name = Books.query.get(book_id).b_name
    msg = f'''
    The Book "{book_name}", has been REVOKED.

    You have been granted 24 hours (or less) notice period to read or download the book. 
    We advice you to visit MyBooks in you Library account to check the final return date of the book.
    
    We are sorry for the inconvinience and thank you for understanding :)
    '''
    sendEmail(user_id=user_id, email_type="info", message=msg)
    return f"Revoke message sent to User ID {user_id}"

@celery.task()
def issue_approval_email(user_id, book_name, status="APPROVED"):
    msg1 = f'Book Name: "{book_name}" \t\t Status: {status}\n\n'
    msg_approve = '''
    Now you can read and download the book from MyBooks section in the application.
    You can also find more information for the issue duration in MyBooks section.
    Happy Reading!!
    '''
    msg_decline = '''
    Unfortunately, we are unable to grant you approval for the book. 
    Please try again after 24 hours.
    '''
    if status=='APPROVED':
        message = msg1+msg_approve
    else:
        message = msg1+msg_decline
    try:
        sendEmail(user_id=user_id, email_type="info", message=message)
    except TypeError as e:
        return str(e)
    return f"Book issue status {status} email sent to User ID {user_id}"