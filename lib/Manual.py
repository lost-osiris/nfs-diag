from write_log import Logger
from auto import Auto
from tcpdump import TcpDump
from data import Data
import os, sys, time

class Manual(object):
   def __init__(self, **kwargs):
      self.data = Data(**kwargs)
      if "server_ip" in kwargs:
         self.server_ip = kwargs['server_ip']

      if "interface" in kwargs:
         self.interface = kwargs['interface']

      if self.server_ip == False and self.interface == False:
         self.server_ip = self.data.find_ip()
         self.interface = []

         for i in self.server_ip: 
            self.interface.append(self.data.find_interface(i))

         self.interactive(self.data)

      if self.server_ip != False and self.interface == False:
         test_ip = self.data.find_ip()

         self.data.test_ip(self.server_ip)
         if self.server_ip not in test_ip:
            self.data.log("No nfs server mounted with specified ip (" + self.server_ip + ")")
            sys.exit()

         interface = self.data.find_interface(self.server_ip)
         self.run(self.server_ip, interface)

      else:
         test_ip = self.data.find_ip()

         self.data.test_ip(self.server_ip)
         if self.server_ip not in test_ip:
            self.data.log("No nfs server mounted with specified ip (" + self.server_ip + ")")
            sys.exit()

         self.run(self.server_ip, self.interface)

   def run(self, ip, interface):
      try:
         output = "Starting Manual Mode"
         self.data.log(output)

         tcp = TcpDump(self.data, ip, interface)
         if tcp.error == False:
            self.data.log("\nIf you want to exit hit \"CTRL + c\"")

            while True:
               time.sleep(0.5)
               if tcp.process_check.is_alive() == False and tcp.process.is_alive() == False:
                  self.data.log("*** Exiting ***")
                  self.data.log("*** Done ***")
                  sys.exit()
               continue

      except KeyboardInterrupt:
         self.data.log("\n*** Exiting ***")
         tcp.kill_tcpdump()
         self.data.log("*** Done ***")
         sys.exit()

      
   def interactive(self, data):
      output = "Starting Manual Mode\n"
      servers = self.data.get_all_servers()

      for (key, value), i in zip(servers.items(), range(0, len(servers))):
         output += "\t" + str(i) +") " + value['server_ip'] + " on " + value['client_mount'] + "\n"
      output += "Which server would you like to test on " + str(range(0, len(servers))) + ": "
     
      options = range(0, len(servers))
  
      user = self.data.log(output, log_input=True)

      while True:
         try:
            user = int(user)
         except:
            self.data.log("\n*** Invalid selection ***\n")
            user = self.data.log(str("Which server would you like to test on " + str(range(0, len(servers))) + ": "), log_input=True)
            continue

         if user in options:
            for key, value in servers.items():
               if value['mapping'] == user:
                  tcp = TcpDump(self.data, value['server_ip'], value['interface'])

                  try:
                     
                     if tcp.error == False: 
                        self.data.log("\nIf you want to exit hit \"CTRL + c\"")

                     while True:
                        time.sleep(0.5)
                        if tcp.process_check.is_alive() == False and tcp.process.is_alive() == False:
                           self.data.log("*** Exiting ***")
                           self.data.log("*** Done ***")
                           sys.exit(1)
                        continue
                  

                  except KeyboardInterrupt:
                     self.data.log("\n*** Exiting ***")
                     tcp.kill_tcpdump()
                     self.data.log("*** Done ***")
                     sys.exit()
         else:
            self.data.log("\n*** Invalid selection ***\n")
            user = self.data.log(str("Which server would you like to test on " + str(range(0, len(servers))) + ": "), log_input=True)

