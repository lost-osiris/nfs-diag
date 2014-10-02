from write_log import Logger
from auto import Auto
from tcpdump import TcpDump
import os, sys, time

class Manual(Auto):
   def __init__(self, **kwargs):

      self.data = {
         'servers': {}
      }

      for key, val in kwargs.items():
         if type(val) == list and len(val) == 1:
            self[key] = val[0]
         else:
            self[key] = val

      if self.location == False:
         self.location = "/tmp/"

      self.logger = Logger(str(self.location + "commandline_output.txt"))

      #interface and ip aren't specified
      if self.server_ip == False and self.interface == False:
         self.server_ip = self.find_ip()
         self.interface = []

         for i in self.server_ip: 
            self.interface.append(self.find_interface(i))

         self.interactive(self.data)
      #ip is specified but interface isn't
      else:
         test_ip = self.find_ip()

         self.test_ip(self.server_ip)
         if self.server_ip not in test_ip:
            self.logger.log("No nfs server mounted with specified ip (" + self.server_ip + ")")
            sys.exit()

         self.interface = self.find_interface(self.server_ip)
         self.run()

   def run(self):
      try:
         output = "Starting Manual Mode"
         self.logger.log(output)

         tcp = TcpDump(self, self.server_ip, self.interface)
         if tcp.error == False:
            self.logger.log("\nIf you want to exit hit \"CTRL + c\"")

            while True:
               time.sleep(0.5)
               if tcp.process_check.is_alive() == False and tcp.process.is_alive() == False:
                  self.logger.log("*** Exiting ***")
                  self.logger.log("*** Done ***")
                  sys.exit()
               continue

      except KeyboardInterrupt:
         self.logger.log("\n*** Exiting ***")
         tcp.kill_tcpdump()
         self.logger.log("*** Done ***")
         sys.exit()

      
   def interactive(self, data):
      mapping = self.data
      output = "Starting Manual Mode\n"
      for (key, value), i in zip(data['servers'].items(), range(0, len(data['servers']))):
         self.data['servers'][key]['mapping'] = i
         output += "\t" + str(i) +") " + value['server_ip'] + " on " + value['client_mount'] + "\n"

      output += "Which server would you like to test on " + str(range(0, len(data['servers']))) + ": "
     
      options = range(0, len(data['servers']))
  
      try:
         user = self.logger.log(output, log_input=True)

         while True:
            try:
               user = int(user)
            except:
               self.logger.log("\n*** Invalid selection ***\n")
               user = self.logger.log(str("Which server would you like to test on " + str(range(0, len(data['servers']))) + ": "), log_input=True)
               continue

            if user in options:
               for key, value in mapping['servers'].items():
                  if value['mapping'] == user:
                     tcp = TcpDump(self, value['server_ip'], value['interface'])

                     try:
                        
                        if tcp.error == False: 
                           self.logger.log("\nIf you want to exit hit \"CTRL + c\"")

                        while True:
                           time.sleep(0.5)
                           if tcp.process_check.is_alive() == False and tcp.process.is_alive() == False:
                              self.logger.log("*** Exiting ***")
                              self.logger.log("*** Done ***")
                              sys.exit(1)
                           continue
                     
 
                     except KeyboardInterrupt:
                        self.logger.log("\n*** Exiting ***")
                        tcp.kill_tcpdump()
                        self.logger.log("*** Done ***")
                        sys.exit()
            else:
               self.logger.log("\n*** Invalid selection ***\n")
               user = self.logger.log(str("Which server would you like to test on " + str(range(0, len(data['servers']))) + ": "), log_input=True)

      except KeyboardInterrupt:
         self.logger.log("\nExiting")
         sys.exit()

