import os, sys

class Logger:
   def __init__(self, location):
      self.location = location
      output_file = open(self.location, "w")
      output_file.close()

   def log(self, *args, **kwargs):
      output = args[0]

      if "log_input" in kwargs:
         log_input = kwargs['log_input']
      else:
         log_input = None
         

      if "no_print" in kwargs:
         no_print = kwargs['no_print']
      else:
         no_print = None

      if log_input == None:
         output_file = open(self.location, "ab+")

         output_file.write(str(output + "\n"))
         output_file.close()
         if no_print == None:
            print (output)
      else:
         output_file = open(self.location, "ab+")
         output_file.write(str(output + "\n"))

         try:
            get_input = raw_input(output)
         except KeyboardInterrupt:
            self.log("\nExiting")
            sys.exit()

         output_file.write(str(get_input + "\n"))
         output_file.close()
         return get_input

