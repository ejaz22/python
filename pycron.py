from subprocess import Popen
from apscheduler.schedulers.background import BackgroundScheduler
import os,pytz,time,datetime,getpass,subprocess
l_user = getpass.getuser()
s = BackgroundScheduler()

def cron_job(txt):
    print "Run Cron ", txt
    Popen(txt,shell=True)

def est_to_gmt(h_str):
    if h_str.find("-")>-1:
        s, e = map(int, h_str.split("-"))
        h_list = list(range(s, e + 1))
    else:
        h_list = map(int, h_str.split(","))
    return ",".join(map(str, [pytz.timezone('US/Eastern').localize(datetime.datetime.now().replace(hour=h)).astimezone(
        pytz.timezone("GMT")).hour for h in h_list]))

# DAILY SCHEDULED
s.add_job(cron_job,'cron',["python /home/user/xyz/abc.py"],
          year = "*",month="*",day="*",hour=est_to_gmt("07"),minute="30",day_of_week="*")
          
s.add_job(cron_job,'cron',["python /home/user/xyz/efg.py"],
          year = "*",month="*",day="*",hour=est_to_gmt("09"),minute="30",day_of_week="mon-fri")  
                    

s.start()

while True:
    time.sleep(3600)
