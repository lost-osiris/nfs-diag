from multiprocessing import Process
import os, sys, argparse, re, subprocess, time, signal
TODO = '''
   1) Actually run tcpdump
   2) Add functionality to check message
   3) Add functionality to allow users to run their own test case
   4) Validate user specified location
   5) When DNS is used to mount server add extra step to send a ping to the server to find interface

'''

script_description = '''
   Script finds NFS servers to run tcpdump on. By default the script runs in 
   manual mode allowing the user to select which server the user would like
   to run on. All output of script will be archived and stored in users current
   directory.
'''

class Auto:
   def __init__(self, location=None, case=None, file_name=None):
      self.auto = True
      self.case = case
      self.location = location
      self.file_name = file_name
      self.data = {
         'servers': {},
      }

      self.find_ip()
      pool = []
      for key, value in self.data['servers'].items():
         ip = key
         interface = self.find_interface(ip)
         TcpDump(self, ip, interface)
         #process = Process(target=TcpDump, args=(self, ip, interface))
         #process.start()
         #print process.pid

   def find_ip(self):
      output = subprocess.Popen(['cat', '/proc/mounts'], stdout=subprocess.PIPE)
      output = output.communicate()[0]
      
      results = output.split("\n")
      regex = re.compile('^(?P<server_ip>^\d+\.\d+\.\d+\.\d+)\:(?P<server_mount>.+?)\s(?P<client_mount>.+?)\s(?P<version>.+?)\s(?P<options>.+)$')
   
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
      output = subprocess.Popen(['ip', 'route', 'get', ip], stdout=subprocess.PIPE)
      output = output.communicate()[0]
      
      results = output.split(" ")
      for i in range(0, len(results)):
         if results[i] == "dev":
            self.data['servers'][ip]['interface'] = results[i+1] 
            return results[i+1]

      return ""

   def get_case(self):
      return self.case

   def get_file_name(self):
      return self.case

   def get_location(self):
      return self.location

class Manual(Auto):

   def __init__(self, interface=None, server_ip=None, location=None, case=None, file_name=None):
      self.interface = interface
      self.ip = server_ip
      self.case = case
      self.location = location
      self.file_name = file_name
      self.data = {
         'servers': {}
      }
      
      if self.ip == None:
         self.ip = self.find_ip()     
      else:
         print self.test_ip(self.ip)

      if self.interface == None:
         self.interface = []
         for i in self.ip:
            self.interface.append(self.find_interface(i))

      self.interactive(self.data)


   def test_ip(self, ip):
      regex = re.compile('(^\d+\.\d+\.\d+\.\d$)')
      results = regex.match(ip)

      if results == None:
         print "The ip address specified (" + ip + ") is not a valid ip address"
         sys.exit(1)

   def interactive(self, data):
      mapping = self.data
      output = "Starting Manual Mode\n"
      for (key, value), i in zip(data['servers'].items(), range(0, len(data['servers']))):
         self.data['servers'][key]['mapping'] = i
         output += "\t" + str(i) +") " + value['server_ip'] + " on " + value['client_mount'] + "\n"

      output += "Which server would you like to test on " + str(range(0, len(data['servers']))) + ": "
     
      options = range(0, len(data['servers']))
   
      user = raw_input(output)
      while True:
         #try:
         user = int(user)
      
         if user in options:
            for key, value in mapping['servers'].items():
               if value['mapping'] == user:
                  tcp = TcpDump(self, value['server_ip'], value['interface'])
                  print "*** Running tcpdump on the following pids: ", tcp.get_pids(), " ***"
                  print "If you want to exit hit \"CTRL + c\""
                  try: 
                     while True:
                        continue
                  except KeyboardInterrupt:
                     print "\nExiting"
                     tcp.stop_tcpdump()
                     print "*** Done ***"
                     sys.exit(1)
            break
         '''
         except:
            print "\n*** Invalid selection ***\n"
            user = raw_input("Which server would you like to test on " + str(range(0, len(data['servers']))) + ": ")
         '''   
      

class TcpDump(Auto, Manual):
   def __init__(self, obj, ip, interface):
      self.file_name = obj.get_file_name()
      self.location = obj.get_location()
      self.case = obj.get_case()
      self.ip = ip
      self.interface = interface

      if self.file_name == None:
         if self.case == None:
            self.file_name = "tcpdump-test-" + self.interface + "-" + self.ip + ".pcap"
         else:
            self.file_name = "tcpdump-test-case#" + self.case + "-" + self.interface + "-" + self.ip + ".pcap"
      else:
         if self.case != None:
            self.file_name = "case#" + file_name
      
      if self.location == None:
         self.location = "/tmp/"
      
      self.pids = {}
      self.output_file = open(str(self.location + "commandline_output.txt"), "w")
      self.sub_process = None

      self.output = self.location + self.file_name

      self.process = Process(target=self.run_tcpdump(), args=())
      self.process.start()
 
      self.pids['parent'] = os.getppid()
      self.pids['main'] = os.getpid()
      self.pids['multiprocessing'] = self.process.pid
 
   def run_tcpdump(self):
      message = "\nTesting Host: " + self.ip
      message += "\nInterface: " + self.interface
      message += "\nOutput Location: " + self.output + "\n"
      print message
      self.tcpdump_command = str('tcpdump -s0 -i ' + self.interface + ' host ' + self.ip + ' -C 1024MB -w ' + self.output)
      self.sub_process = subprocess.Popen([self.tcpdump_command], shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE) 

      self.pids['subprocess'] = self.sub_process.pid
      if self.sub_process.returncode != None:
         print "Error running tcpdump\n"
         print "Tcpdump Error: \"%s\"\n" % self.sub_process.communicate()[1].replace("\n", "")
         print "Exiting script"
         sys.exit(1)

   def stop_tcpdump(self):
      self.sub_process.terminate()

      self.output_file.write(str("Tcpdump command: \"" + self.tcpdump_command + "\"\n"))
      self.output_file.write(str(self.sub_process.communicate()[1] + "\n"))

      self.output_file.close()
      self.process.terminate()

   def get_pids(self):
      return self.pids.values()
            
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description=script_description)

   dest = 'Will run TCP dump on all servers mounted by NFS'
   parser.add_argument('-a', '--auto', help=dest, action='store_true')

   dest = 'Must specify NFS server IP address. Script finds interface for TCP dump with supplied IP address.'
   parser.add_argument('-s', '--server_ip', help=dest,type=str)

   dest = '''
   Must supply valid case number
   Takes case number and apply
   it to output file of TCP dump.
   '''
   parser.add_argument('-c', '--case_number', help=dest,type=str)

   dest = '''The name of the .pcap file that will be outputed'''
   parser.add_argument('-f', '--file_name', help=dest,type=str)

   dest = '''The location where all files will be outputed'''
   parser.add_argument('-l', '--location', help=dest,type=str)

   dest = '''
      Must specify an interface for TCP dump to run on. 
      Script will find server mounted by specified interface.
   '''   
   parser.add_argument('-i', '--interface', help=dest,type=str)

   args = parser.parse_args()

   if args.auto and (args.server_ip == True or args.interface == True):
      print "Can't run Manual mode and Auto mode at the same time"
   elif args.auto:
      Auto(case=args.case_number, file_name=args.file_name, location=args.location)
   elif args.server_ip != None or args.interface != None:
      Manual(interface=args.interface, server_ip=args.server_ip, case=args.case_number, file_name=args.file_name, location=args.location)
   else:
      Manual(case=args.case_number, file_name=args.file_name, location=args.location)



