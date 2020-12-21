from apscheduler.schedulers.background import BackgroundScheduler
from In_out.interrupts.inter.Interrupt import Interrupt
from datetime import datetime

class Interrupt_cron(Interrupt):
    """
    Permet de schedule des interruptions
    """
    def __init__(self, name, name_env, date, client):
        Interrupt.__init__(self, name, name_env, client)
        self.date = date
        self.sched = BackgroundScheduler()

    def start(self):
        hour, minutes, second = self.date.split(":", 3)
        now = datetime.now().time()
        try:
            # if the hour is already pass today, just do it
            # /!\ need to define the cron in data in the order of time
            if int(hour) < int(now.hour) or (int(hour) == int(now.hour) and int(minutes) < int(now.minute)):
                self.press()
        except:
            pass
        self.sched.add_job(self.press, 'cron', hour=hour, minute = minutes, second = second)
        self.sched.start()




    def __str__(self):
        return "type : cron | date : {}".format(self.date)
