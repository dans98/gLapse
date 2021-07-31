from glapse.lapse.interconnects.abstract import Abstract
from tornado.httpclient import HTTPRequest
import pycurl, json

## the class used to interact with standalone duet control boards 
#
# a simple abstract class that provides the methods needed to communicate with a printer  
class StandaloneDuet(Abstract):
    ## The init does what an init normally does 
    #
    # @param self The object pointer
    # @param printerSettings a glapse.settings.printersettings.PrinterSettings object
    def __init__(self, printerSettings):
        super(StandaloneDuet,self).__init__(printerSettings)

        checkRequestUrl = self.printerSettings.printerbaseUrl + 'rr_status?type=1'
        args = {
            'method' : 'GET', 
            'decompress_response' : False,
            'prepare_curl_callback' : lambda c: c.setopt(pycurl.TCP_FASTOPEN, 1)
        }

        ## @var checkRequest
        # a tornado.httpclient.HTTPRequest object
        self.checkRequest = HTTPRequest(checkRequestUrl, **args)

    ## opens a connection to the printer 
    #
    # @param self The object pointer
    # @returns a bool indicating if a connection was made to the printer 
    async def connect(self):
        url = self.printerSettings.printerbaseUrl + 'rr_connect?password=' + self.printerSettings.printerpassword
        response = await self.client.fetch(url, method='GET')

        if response.code == 200:  
            return True
        else:
            return False

    ## polls the printer for messages
    #
    # @param self The object pointer
    # @returns a boolean false if no message was returned from the printer or the message as a string
    async def checkForMessages(self):
        response = await self.client.fetch(self.checkRequest)

        if response.code == 200:  
            output = json.loads(response.body)

            if('output' in output):
                if('msgBox' in output['output']):
                    if('msg' in output['output']['msgBox']):
                        return output['output']['msgBox']['msg'] 
                    else:
                        return '' 
                else:
                    return ''        
            else:
                return ''
        else:
            return False

    ## tells the printer to resume printing
    #
    # @param self The object pointer
    # @returns a boolean false on failure, true otherwise
    async def resumePrint(self):
        url = self.printerSettings.printerbaseUrl + 'rr_gcode?gcode=M292' 
        response = await self.client.fetch(url, method='GET')

        if response.code == 200: 
            return True
        else:
            return False