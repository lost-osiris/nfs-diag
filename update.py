import os, sys, subprocess, inspect

PIPE = subprocess.PIPE
class Update(object):

   def __init__(self):
      path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

      self.full_path = ""
      for i in path.split("/"):
         if "/" in i:
            self.full_path += i.replace("/", "")
         elif i == "current":
            continue
         else:
            self.full_path += str(i + "/")

      self.orginal_path = self.full_path
      self.full_path += "repo/.git"

   def update(self):
         blah = self.check_update()
         print blah

         '''   
         rm = subprocess.Popen(["rm", "-f", str(orginal_path + "current/*.pyc"), ], stdout=PIPE, stderr=PIPE)
         rm = subprocess.Popen(["rm", "-f", str(orginal_path + "current/*.pyo"), ], stdout=PIPE, stderr=PIPE)
         rm = subprocess.Popen(["rm", "-f", str(orginal_path + "repo/*.pyc"), ], stdout=PIPE, stderr=PIPE)
         rm = subprocess.Popen(["rm", "-f", str(orginal_path + "repo/*.pyo"), ], stdout=PIPE, stderr=PIPE)

         if "error" in output[0].lower() or "error" in output[1].lower():
            print "Type: ", output[1]
         elif "up-to-date" in str(output[0]) or "up-to-date" in str(output[1]):
            self._set_error("already up-to-date")
            return False
         else:
            copy = subprocess.Popen(["cp", str(orginal_path + "repo/*"), str(orginal_path + "current")], stdout=PIPE, stderr=PIPE)
            return True
         '''
   def check_update(self):
      process = subprocess.Popen(["git", str("--git-dir=" + self.full_path), "remote", "update"], stdout=PIPE, stderr=PIPE)
      process = subprocess.Popen(["git", str("--git-dir=" + self.full_path), "status", "-uno"], stdout=PIPE, stderr=PIPE)
      output = process.communicate()[0]
      update = False
      for i in output:
         if "#" in i and "behind" in i:
            update = True
      print output
      return update

   def _set_error(self, message):
      self.error = message

   def get_error(self):
      return self.error
