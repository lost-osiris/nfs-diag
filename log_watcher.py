import os, sys, time, multiprocessing

class LogWatcher:
   def __init__(self, location=None, messages=None):
      self.default_messages = ["timed out", "not responding"]

      if messages != None:
         messages = message.split(",")
         for i in messages:
            self.default_messages.append(i)
      
      if location == None:
         self.location = ["/var/log/messages"]

      else:
         self.location = location.split(",")

      pool = []
      for i in self.location:
         j = multiprocessing.Process(target=self.watch, args=(i,))
         pool.append(j)
         j.start()

      done = True
      while done:
         count = 0

         for i in pool:
            if i.is_alive() == False:
               count += 1

            if count == len(pool):
               done = False

      print "finished"
         
   def watch(self, location):
      target = open(location)
      while 1:
         where = target.tell()
         line = target.readline()
         if not line:
            time.sleep(1)
            target.seek(where)
         else:
            current_time = time.strftime("%H:%M")
            current_date = time.strftime("%b %d")
            for i in self.default_messages:
               if i in line and current_time in line and current_date in line:
                  return
            
if __name__ == "__main__":
   LogWatcher() 
