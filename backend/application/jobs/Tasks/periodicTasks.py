from datetime import datetime, date
from ..workers import celery
from flask_sse import sse
from celery.schedules import crontab

from utils.sendEmails import sendEmail
from application.database import db
from application.models.users import Users
from application.models.user_book_activity import IssueRequest
from application.models.users import Users

# print("crontab ", crontab)

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=22, minute=31), 
                             daily_reminder.s(), name='Daily Reminder for not active Users')
    sender.add_periodic_task(crontab(hour=22, minute=33, day_of_month='7', month_of_year='*'), 
                             monthly_activity_report.s(), name='Monthly User Activity Report')
    sender.add_periodic_task(crontab(hour=22, minute=34), 
                             issue_clean_up.s(), name='Cleaning non pending Issue Requests')

## Delete IssueRequest if not PENDING - Celery (Once a day)
@celery.task()
def issue_clean_up():
    issues = IssueRequest.query.all()
    count = 0
    for i in issues:
        if i.status!=2:
            db.session.delete(i)
            count+=1
        elif not Users.query.get(i.user_id):
            db.session.delete(i)
            count+=1
    db.session.commit()
    print(f'Deleted {count} issue_request. Remaining {len(issues)-count} pending issues.')

@celery.task()
def daily_reminder():
    users = Users.query.all()
    count = 0
    for user in users:
        print(user)
        if user.id!=1:
            today = datetime.now().strftime("%d/%m/%Y")
            # print(user.latest_activity)
            activity = user.latest_activity
            # print(today, activity)
            if (activity is None) or (today!=activity.strftime("%d/%m/%Y")):
                sendEmail(user.id)
                count+=1
    print('Sent Emails to '+ str(count)+' people out of total '+str(len(users)-1))   

@celery.task()
def monthly_activity_report():
    users = Users.query.all()
    for user in users: 
        if user.id!=1:
            sendEmail(user.id, email_type='report')
    print('Sent all monthly reports')
