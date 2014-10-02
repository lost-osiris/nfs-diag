from write_log import Logger
class Error(object):
   def __init__(self, error_type, log_location):
      self.__set_error(error_type)
      Logger(log_location).log(error_type.get_error_message())

      if type(self.get_error()) == InvalidIp:
         sys.exit()

      return self.get_error()
         
   def __set_error(self, error_type):
      self.error = error_type

   def get_error(self):
      return self.error

class InvalidIp(object):
   def __init__(self, message=None):
      if message == None
         self.message = "Invalid Ip Specified."
      else:
         self.message = message

   def get_error_message(self):
      return self.message

class FilePathNotFound(object):
   def __init__(self, message=None):
      if message == None
         self.message = "File Path specified does not exist."
      else:
         self.message = message

   def get_error_message(self):
      return self.message
