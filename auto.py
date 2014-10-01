from multiprocessing import Process
from tcpdump import TcpDump
from write_log import Logger
import os, sys, re, subprocess, time

PIPE = subprocess.PIPE
class Auto(object):
   def __init__(self, **kwargs):

      for key, val in kwargs.items():
         self[key] = val   

      if self.location == False:
         self.location = "/tmp/"

      self.logger = Logger(str(self.location + "commandline_output.txt"))
      self.run()

   def __setitem__(self, key, value):
      self.__dict__[key] = value
   def __getitem__(self, key):
      return self.__dict__[key]

   def run(self):
      self.data = {
         'servers': {},
      }

      self.find_ip()
      pool = []
      self.logger.log("If you want to exit hit \"CTRL + c\"")
      for key, value in self.data['servers'].items():
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

   def find_ip(self):
      output = subprocess.Popen(str('cat ' + "/proc/mounts"),shell=True, stdout=PIPE, stderr=PIPE)
      results = output.communicate()[0].split("\n")
      regex = re.compile('^(?P<server_ip>^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]))\:(?P<server_mount>.+?)\s(?P<client_mount>.+?)\s(?P<version>.+?)\s(?P<options>.+)$')
   
      ip = []
      for i in results:
         found = regex.match(i)
         if found != None:
            server = {
               'server_ip': found.group('server_ip'),
               'server_mount': found.group('server_mount'),
               'client_mount': found.group('client_mount'),
               'version': found.group('version'),
               'options': found.group('options').split(","),
            }

            self.data['servers'][server['server_ip']] = server
            ip.append(server['server_ip'])  

      if len(ip) > 0: 
         return ip
      else:
         return None

   def find_interface(self, ip):
      output = subprocess.Popen(str('ip route get ' + ip),shell=True, stdout=PIPE)
      output = output.communicate()[0]
      
      results = output.split(" ")
      for i in range(0, len(results)):
         if results[i] == "dev":
            self.data['servers'][ip]['interface'] = results[i+1] 
            return results[i+1]

      return ""

   def test_ip(self, ip):
      regex = re.compile('(^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$)')
      results = regex.match(ip)

      if results == None:
         self.logger.log(str("The ip address specified (" + ip + ") is not a valid ip address"))
         sys.exit()
   
      ping = subprocess.Popen([str('ping -c 1 -w 1 -q ' + ip + " | grep packet | awk '{ print $1; print $4 }'")], shell=True, stdout=PIPE, stderr=PIPE)

      results = ping.stdout.readlines()
      if results[0] != results[1]:
         self.logger.log(str("Server Ip specified (" + self.ip +") timed out. Exiting"))
         sys.exit()

   def get_case(self):
      return self.case_number

   def get_file_name(self):
      return self.file_name

   def get_location(self):
      return self.location

