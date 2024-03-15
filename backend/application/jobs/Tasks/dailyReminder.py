from datetime import datetime, date
from ..workers import celery
from flask_sse import sse
from celery.schedules import crontab

from utils.sendEmails import sendEmail
from application.database import db
from application.models.users import Users

print("crontab ", crontab)

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    #sender.add_periodic_task(2.0, print_current_time_job.s(), name='add every 10')
    sender.add_periodic_task(crontab(hour=22, minute=43), 
                             daily_reminder.s(), name='Daily Reminder for not active Users')

@celery.task()
def daily_reminder():
    users = Users.query.all()
    count = 0
    for user in users:
        if user.id!=1:
            today = datetime.now().strftime("%d/%m/%Y")
            activity = user.latest_activity.strftime("%d/%m/%Y")
            print(today, activity)
            if today!=activity:
                sendEmail(user.id)
                count+=1
    print('Sent Emails to', count, 'people out of total', len(users)-1)   

## Test Task
@celery.task()
def print_current_time_job():
    print("START")
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string) 
    print("COMPLETE")