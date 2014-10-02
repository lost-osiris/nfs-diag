import os, sys

class Logger:
   def __init__(self, location):
      self.location = location
      output_file = open(self.location, "w")
      output_file.close()

   def log(self, output, log_input=None, no_print=None):
      if log_input == None:
         output_file = open(self.location, "ab+")
         output_file.write(str(output + "\n"))
         output_file.close()
         if no_print == None:
            print (output)
      else:
         output_file = open(self.location, "ab+")
         output_file.write(str(output + "\n"))

         get_input = raw_input(output)
         output_file.write(str(get_input + "\n"))
         output_file.close()
         return get_input

