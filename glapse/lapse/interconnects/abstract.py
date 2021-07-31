from glapse.exception.raiser import Raiser
from tornado.httpclient import AsyncHTTPClient

AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')

## a simple abstract/base class
#
# a simple abstract class that provides the methods needed to communicate with a printer  
class Abstract(Raiser):

    ## The init does what an init normally does 
    #
    # @param self The object pointer
    # @param printerSettings a glapse.settings.printersettings.PrinterSettings object
    def __init__(self, printerSettings):

        ## @var printerSettings
        # a glapse.settings.printersettings.PrinterSettings object
        self.printerSettings = printerSettings

        ## @var client
        # a tornado.httpclient.AsyncHTTPClient object
        self.client = AsyncHTTPClient()

    ## the method that should be used to open a connection to the printer 
    #
    # @param self The object pointer
    # @returns a bool indicating if a connection was made to the printer 
    async def connect(self):
        return False

    ## the method that should be used to poll the printer for messages
    #
    # @param self The object pointer
    # @returns a boolean false if no message was returned from the printer or the message as a string
    async def checkForMessages(self):
        return False

    ## the method that should be use to tell the printer to resume printing
    #
    # @param self The object pointer
    # @returns a boolean false on failure, true otherwise
    async def resumePrint(self):
        return False