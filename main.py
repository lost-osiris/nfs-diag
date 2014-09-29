from auto import Auto
from manual import Manual
from write_log import Logger
import os, sys, argparse, subprocess, inspect

features = '''
   1) Has an interactive mode
   2) Auto mode runs tcpdump on all server mounts
   3) RPM is available for script
   4) Check to see if server specified is a NFS mounted server
   5) Detects if tcpdump is running if not it kills script
      will only kill the script if ALL of the tcpdumps that are running are closed
   6) Tests the server that tcpdump is trying to run on to make sure the client can reach the server
   !) Archives all the files that script outputs
   8) Detects if current user has permissions to interface
   !) Checks logs and determines if NFS server timed out in a certian amount of time
   !) Updates automatically
   $) Validate user input  
      $  a. Any path specified
         b. Any Ip's
      !  c. Case number
      !  d. Interface
   !) Lists all data on current NFS servers
'''

script_description = '''
   Script finds NFS servers to run tcpdump on. By default the script runs in 
   manual mode allowing the user to select which server the user would like
   to run on. All output of script will be archived and stored in users current
   directory.
'''

def check_log(args):
   print ("check_log\n", vars(args))

def auto(args):
   print ("Auto\n", vars(args))

def manual(args):
   print ("Manual\n", vars(args))

PIPE = subprocess.PIPE

if __name__ == '__main__':
   parser = argparse.ArgumentParser(description=script_description)

   dest = 'Will run TCP dump on all servers mounted by NFS'
   parser.add_argument('-a', '--auto', help=dest, action='store_true')

   dest = '''
   Must supply valid case number
   Takes case number and apply
   it to output file of TCP dump.
   '''
   parser.add_argument('-c', '--case_number', help=dest, nargs=1, type=str, default=False)

   dest = '''The name of the .pcap file that will be outputed'''
   parser.add_argument('-f', '--file_name', help=dest, nargs=1, type=str, default=False)

   dest = '''The location where all files will be outputed'''
   parser.add_argument('-l', '--location', help=dest, nargs=1, type=str, default=False)

   dest = '''
      Specify a list of files to check for either specified strings or default.
   '''
   parser.add_argument("-F", "--log_files", help=dest, nargs="?", type=str, default="/var/log/messages")

   dest = '''
      Check logs for messages. Will use default logs and messages if they aren't specified.
   '''
   parser.add_argument("-C", "--check_log", help=dest, type=str, default=False)

   dest = '''
      A .csv file can be specified to check log files with a set of strings.
   '''
   messages = ["timed, out", "not responding"] 
   parser.add_argument("-m", "--messages", help=dest, nargs="?", type=str, default=messages)

   dest = 'Must specify NFS server IP address. Script finds interface for TCP dump with supplied IP address.'
   parser.add_argument('-s', '--server_ip', help=dest, nargs=1, type=str, default=False)

   dest = '''
      Must specify an interface for TCP dump to run on. 
      Script will find server mounted by specified interface.
   '''
   parser.add_argument('-i', '--interface', help=dest, nargs=1, type=str, default=False)

   dest = '''
      Updates the script.
   '''
   parser.add_argument('-u', '--update', help=dest, action="store_true", default=False)
   args = parser.parse_args()

   if args.update == True:
      path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

      full_path = "/"
      for i in path.split("/"):
         if "/" in i:
            full_path += i.replace("/", "")
         else:
            full_path += str(i + "/")

      work_tree = full_path
      full_path += "/.git"

      process = subprocess.Popen(["git", str("--git-dir=" + full_path), "pull"], stdout=PIPE, stderr=PIPE)
         
      output = process.communicate()
      if "permissions denied" in output[0].lower() or "permissions denied" in output[1].lower():
         print "You do not have permissions to update script. Run script with sudo permissions"
      elif "error" in output[0].lower() or "error" in output[1].lower():
         print "Error updating script"
         print ("Type: ", output[1])
      elif "already up-to-date" in output[0].lower() or "already up-to-date" in output[1].lower():
         print "Script is already up-to-date"
      else:
         print "*** 1Successfully updated ***"
      print full_path
      print output
   elif args.auto and (args.server_ip != False or args.interface != False):
      print ("Can't run Manual mode and Auto mode at the same time")
   elif args.auto:
      Auto(**vars(args))
   elif args.server_ip != False and args.interface != False:
      Manual(**vars(args))
   elif args.server_ip == False and args.interface != False:
      print ("You must specify a server_ip if you are going to specify an interface.\nIf you already know the server_ip the script with find the proper interface")
   elif args.server_ip != False and args.interface == False:
      Manual(**vars(args))
   else:
      Manual(**vars(args))


