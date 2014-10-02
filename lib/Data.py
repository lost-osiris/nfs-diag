from write_log import Logger
import ErrorType
import os, sys, re, subprocess, time

PIPE = subprocess.PIPE

class Data(object):
   def __init__(self, **kwargs):
      self.data = {'servers': {}, }      

      for key, val in kwargs.items():
         self[key] = val

      if self.location == False:
         self.location = "/tmp/"

      self.log_file = str(self.location + "commandline_output.txt")
      self.logger = Logger(self.log_file) 

      self.find_ip()
       
   def __setitem__(self, key, value):
      self.__dict__[key] = value
   def __getitem__(self, key):
      return self.__dict__[key]

   def find_ip(self):
      output = subprocess.Popen(str('cat ' + "/proc/mounts"),shell=True, stdout=PIPE, stderr=PIPE)
      results = output.communicate()[0].split("\n")
      regex = re.compile('^(?P<server_ip>^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]))\:(?P<server_mount>.+?)\s(?P<client_mount>.+?)\s(?P<version>.+?)\s(?P<options>.+)$')

      ip = []
      count = 0
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
            self.data['servers'][server['server_ip']]['mapping'] = count
            count += 1
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
         error = ErrorType.InvalidIp()
         ErrorType.Error(error, self.log_file)

      ping = subprocess.Popen([str('ping -c 1 -w 1 -q ' + ip + " | grep packet | awk '{ print $1; print $4 }'")], shell=True, stdout=PIPE, stderr=PIPE)

      results = ping.stdout.readlines()
      if results[0] != results[1]:
         message = str("Server Ip specified (" + ip +") timed out. Exiting")
         error = ErrorType.InvalidIp(message=message)
         ErrorType.Error(error, self.log_file)

   def log(self, *args, **kwargs):
      self.logger.log(args[0], kwargs)

   def get_case(self):
      return self.case_number

   def get_file_name(self):
      return self.file_name

   def get_location(self):
      return self.location

   def get_server(self, server_ip):
      if server_ip in self.data['servers']:
         return self.data['servers'][server_ip]
      else: 
         return None

   def get_all_servers(self):
      return self.data['servers']
      
   def get_interface(self, server_ip):
      if server_ip in self.data['servers']:
         return self.data['servers'][server_ip]['interface']
      else: 
         return None

