from multiprocessing import Process
from tcpdump import TcpDump
from write_log import Logger
from data import Data
import os, sys, re, subprocess, time

PIPE = subprocess.PIPE
class Auto(object):
   def __init__(self, **kwargs):
      self.data = Data(**kwargs)

      self.run()

   def __setitem__(self, key, value):
      self.__dict__[key] = value
   def __getitem__(self, key):
      return self.__dict__[key]

   def run(self):
      pool = []
      self.data.log("If you want to exit hit \"CTRL + c\"")
      for key, value in self.data.get_all_servers().items():
         ip = key
         interface = self.data.find_interface(ip)
         tcp = TcpDump(self.data, ip, interface)
         pool.append(tcp)
         
      try: 
         while True:
            count = 0
            for i in pool:
               if i.process.is_alive() == False and i.process_check.is_alive() == False:
                  count += 1

            if count == len(pool):
               self.data.log("\n*** Exiting ***")
               sys.exit()

            continue
      except KeyboardInterrupt:
         self.data.log("\n*** Exiting ***")
         for i in pool:
            i.kill_tcpdump()
         self.data.log("\n*** Done ***")
         sys.exit()

