import os, sys, time, multiprocessing, subprocess

class LogWatcher:
   def __init__(self, location, messages, pids, obj):
      if type(location) == str:
         self.location = [location]
      else:
         self.location = location

      self.messages = messages
      self.pids = pids
      self.obj = obj
      pool = []
      for i in self.location:
         j = multiprocessing.Process(target=self.watch, args=(i,))
         pool.append(j)
         j.start()

      try:
         done = True
         while done:

            for i in pool:
               if i.is_alive() == False:
                  done = False

         subprocess.Popen(str("kill" + " -9 " + str(self.pids)), shell=True)
         
      except KeyboardInterrupt:
         pass

   def watch(self, location):
      try:
         target = open(location)
         while 1:
            where = target.tell()
            line = target.readline()
            if not line:
               time.sleep(1)
               target.seek(where)
            else:
               current_time = time.strftime("%H:%M")
               current_month = time.strftime("%b")
               current_day = str(int(time.strftime("%d")))
               current_date = str(current_month + "  " + current_day)
               for i in self.messages:
                  
                  if i in line and current_time in line and current_date in line:
                     self.obj.logger.log(str("\nFound message \"" + i + "\" in " + location + "\nKilling tcpdump"))
                     return
      except KeyboardInterrupt:
         return
