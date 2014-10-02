from multiprocessing import Process
from tcpdump import TcpDump
from write_log import Logger
from data import Data
import os, sys, re, subprocess, time

PIPE = subprocess.PIPE
class Auto(object):
   def __init__(self, **kwargs):
      self.logger = Logger(str(self.location + "commandline_output.txt"))

      self.data = Data(kwargs)

      self.run()

   def __setitem__(self, key, value):
      self.__dict__[key] = value
   def __getitem__(self, key):
      return self.__dict__[key]

   def run(self):
      pool = []
      self.logger.log("If you want to exit hit \"CTRL + c\"")
      for key, value in self.data.get_all_servers().items():
         ip = key
         interface = self.find_interface(ip)
         tcp = TcpDump(self, ip, interface)
         pool.append(tcp)
         
      try: 
         while True:
            count = 0
            for i in pool:
               if i.process.is_alive() == False and i.process_check.is_alive() == False:
                  count += 1

            if count == len(pool):
               self.logger.log("\n*** Exiting ***")
               sys.exit()

            continue
      except KeyboardInterrupt:
         self.logger.log("\n*** Exiting ***")
         for i in pool:
            i.kill_tcpdump()
         sys.exit()

