from multiprocessing import Process
from log_watcher import LogWatcher 
import os, sys, time, select, subprocess

PIPE = subprocess.PIPE
class TcpDump(object):
   def __init__(self, obj, ip, interface):
      self.file_name = obj.get_file_name()
      self.location = obj.get_location()
      self.case = obj.get_case()
      self.ip = ip
      self.interface = interface
      self.obj = obj

      if self.file_name == False:
         if self.case == False:
            self.file_name = "tcpdump-test-" + self.interface + "-" + self.ip + ".pcap"
         else:
            self.file_name = "tcpdump-test-case#" + self.case + "-" + self.interface + "-" + self.ip + ".pcap"
      else:
         if self.case != False:
            self.file_name = "case#" + file_name

      if self.location == False:
         self.location = "/tmp/"


      self.execute()

   def execute(self):
      self.pids = {}
      self.sub_process = None

      self.output = self.location + self.file_name

      if self.obj.test_ip(self.ip) != False:
         self.process = Process(target=self.run_tcpdump(), args=())
         self.process_check = Process(target=self.check_tcpdump, args=())

         self.process.start()
         self.process_check.start()
         self.pids['parent'] = os.getppid()
         self.pids['main'] = os.getpid()
         self.pids['multiprocessing'] = self.process.pid
         self.pids['check_tcpdump'] = self.process_check.pid
         return

   def check_tcpdump(self):
      if self.obj.check_log == True:
         process = Process(target=LogWatcher, args=(self.obj.log_files, self.obj.messages, self.pids['subprocess'], self.obj))
         process.start()

      while True:
         check = self.check_pid(self.pids['subprocess'])
         if check == True:
            continue
         elif check == False:
            message = "\n*** Tcpdump on HOST (" + self.ip + ") and on INTERFACE (" + self.interface + ") has STOP ***\n"
            message += "Time Ended: " + time.strftime("[%X %x TimeZone: %Z]") + "\n"

            if self.error == True:
               message += "\nError running tcpdump\n"
               message += "Tcpdump Error: \"%s\"\n" % self.error_data.replace("\n", "")
               message += "Tcpdump Command: \"%s\"" % ' '.join(map(str,self.tcpdump_command))
            self.obj.logger.log(message)

            self._stop_tcpdump()

            break
         else:
            break

   def run_tcpdump(self):       
      message = "\nTesting Host: " + self.ip
      message += "\nInterface: " + self.interface
      message += "\nOutput Location: " + self.output + "\n"
      self.tcpdump_command = ['tcpdump', '-s0', '-i', self.interface, 'host', self.ip, '-C', '1024MB', '-w', self.output]

      self.obj.logger.log(message)
      self.sub_process = subprocess.Popen(self.tcpdump_command, shell=False, stdout=PIPE, stderr=PIPE, stdin=PIPE)

      message = str("*** " + time.strftime("[%X %x TimeZone: %Z]") + " Running tcpdump on the following pid: " + str(self.sub_process.pid) + " ***")
      self.obj.logger.log(message)

      r, w, e = select.select([self.sub_process.stderr], [self.sub_process.stdout], [], 2)
      r2, w2, e2 = select.select([self.sub_process.stdout], [], [], 1)

      if ((self.sub_process.stdout in r2) == False) and ((self.sub_process.stderr in r) == True):
         data = ""
      elif ((self.sub_process.stdout in r2) == True) and ((self.sub_process.stderr in r) == True):
         data = self.sub_process.stderr.read()
      else:
         data = ""

      if data != "" or data == "Error" :
         self.error = True
         self.error_data = data
      else:
         self.error = False

      self.pids['subprocess'] = self.sub_process.pid

   def _stop_tcpdump(self):
      if self.error == False:
         output = ""
         for i in self.sub_process.stderr:
            output += str(i)

         self.tcpdump_output = str("\nTcpdump Command: \"" + ' '.join(map(str,self.tcpdump_command)) + "\"\n" + output)

         self.obj.logger.log(self.tcpdump_output, no_print=True)

      try:
         self.sub_process.terminate()
      except:
         pass

      try:
         self.process.terminate()
      except:
         pass

      try:
         self.process_check.terminate()
      except:
         pass

   def kill_tcpdump(self):
      output = ""
      for i in self.sub_process.stderr:
         output += str(i)

      self.tcpdump_output = str("\nTcpdump Command: \"" + ' '.join(map(str,self.tcpdump_command)) + "\"\n" + output)

      self.obj.logger.log(self.tcpdump_output, no_print=True)

      sys.stdout.flush()
      sys.stderr.flush()

      self.sub_process.terminate()
      self.process_check.terminate()
      self.process.terminate()

   def get_pid(self):
      return str(self.pids['subprocess'])

   def check_pid(self, pid):
      command = str('ps -o stat ' + str(pid))
      ps = subprocess.Popen(command, stdout=PIPE, shell=True)

      try:
         data = ""
         for i in ps.stdout.read():
            data += i
      except:
         return None

      sys.stdout.flush()
      if data != "":
         data = data.split("\n")[1]
      if "Z" in data or "T" in data:
         self.is_done = True
         return False
      else:
         return True

