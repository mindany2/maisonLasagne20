from apscheduler.schedulers.background import BackgroundScheduler
from In_out.interruptions.inter.Interruption import Interruption, TYPE_INTER
from datetime import datetime

class Interruption_date(Interruption):
    """
    Permet de schedule des interruptions
    """
    def __init__(self, nom, date, client, type_inter):
        Interruption.__init__(self, nom, client, type_inter)
        self.date = date
        self.sched = BackgroundScheduler()
        if type_inter == TYPE_INTER.cron:
            heure, minutes, seconde = self.date.split(":")
            now = datetime.now().time()
            try:
                if int(heure) < int(now.hour) or (int(heure) == int(now.hour) and int(minutes) < int(now.minute)):
                    self.press()
            except:
                pass
            self.sched.add_job(self.press, 'cron', hour=heure, minute = minutes, second = seconde)
        self.sched.start()

