import os

from apscheduler.schedulers.blocking import BlockingScheduler
from main import main

type_job = os.environ['TYPE_JOB']

scheduler = BlockingScheduler(timezone=os.environ['TIMEZONE'])

if type_job == 'interval':
    scheduler.add_job(main, "interval", minutes=int(os.environ['SCHULER_MINUTES']))
    scheduler.start()
elif type_job == 'cron':
    scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=17)
    scheduler.start()
else:
    print('Job type not set for scheduler')