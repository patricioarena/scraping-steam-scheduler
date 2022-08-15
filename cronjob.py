import os

from apscheduler.schedulers.blocking import BlockingScheduler
from main import main

try:
    type_job = os.environ['TYPE_JOB']
    scheduler = BlockingScheduler(timezone=os.environ['TIMEZONE'])
    if type_job == 'interval':
        scheduler.add_job(main, "interval", minutes=int(os.environ['SCHULER_MINUTES']))
    elif type_job == 'cron':
        hour_minutes = os.environ['RUN_TIME'].split(':')
        scheduler.add_job(main, 'cron', day_of_week='mon-fri', hour=int(hour_minutes[0]), minute=int(hour_minutes[1]))
    scheduler.start()

except Exception as e:
    print(e)

