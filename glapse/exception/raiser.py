import datetime

# a simple class that allows exceptions raised by the class to be consistently formatted   
class Raiser(object):
    ## the method that raises the exception 
    #
    #  @param self The object pointer
    #  @param msg the message to use when raising the exception
    def raiseException(self, msg):
        time = datetime.datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
        raise Exception(time + " - " + msg)