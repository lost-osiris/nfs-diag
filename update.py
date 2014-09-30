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
      self.error = ""

   def update(self):
         check_update = self.check_update()
         message = ""
         updated = False
         if check_update == True:
            process = subprocess.Popen(["git", str("--git-dir=" + self.full_path), "pull"], stdout=PIPE, stderr=PIPE)
            print process.communicate()
            rm = subprocess.Popen(["rm", "-f", str(self.orginal_path + "current/*.pyc"), ], stdout=PIPE, stderr=PIPE)
            rm = subprocess.Popen(["rm", "-f", str(self.orginal_path + "current/*.pyo"), ], stdout=PIPE, stderr=PIPE)
            rm = subprocess.Popen(["rm", "-f", str(self.orginal_path + "repo/*.pyc"), ], stdout=PIPE, stderr=PIPE)
            rm = subprocess.Popen(["rm", "-f", str(self.orginal_path + "repo/*.pyo"), ], stdout=PIPE, stderr=PIPE)

            copy = subprocess.Popen(["cp", str(self.orginal_path + "repo/*"), str(self.orginal_path + "current")], stdout=PIPE, stderr=PIPE)
             
         elif self.error == "":
            message = "Already up-to-date"
         else:
            message = self.get_error

         return updated, message

   def check_update(self):
      process = subprocess.Popen(["git", str("--git-dir=" + self.full_path), "remote", "update"], stdout=PIPE, stderr=PIPE)
      process = subprocess.Popen(["git", str("--git-dir=" + self.full_path), "status", "-uno"], stdout=PIPE, stderr=PIPE)
      output = process.communicate()
      update = False
      if output[1] != '':
         self._set_error(output[1])
      else:
         for i in output[0].split("\n"):
            if "#" in i and "behind" in i:
               update = True
      return update

   def _set_error(self, message):
      self.error = message

   def get_error(self):
      return self.error
