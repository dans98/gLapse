from glapse.settings.abstract import Abstract

## stores and validates settings needed to generate a sequence of stills
class PrinterSettings(Abstract):
    ## The init does what an init normally does 
    #
    # @param self The object pointer
    # @param input a dict of settings to store and validate
    def __init__(self, input):
        super(PrinterSettings,self).__init__(input)

    ## validates the settings  
    #
    # @param self The object pointer
    # @throws exception id a setting fails validation 
    def validate(self):
        if not hasattr(self, 'printerbaseUrl'):
            self.raiseException('printerbaseUrl is a required setting')

        if not hasattr(self, 'printerpassword'):
            self.raiseException('printerpassword is a required setting')

        if not hasattr(self, 'printerType'):
            self.raiseException('printerType is a required setting')

        if not isinstance(self.printerbaseUrl, str):
            self.raiseException('printerbaseUrl must be a string')

        if not isinstance(self.printerpassword, str):
            self.raiseException('printerpassword must be a string')

        if not isinstance(self.printerType, str):
            self.raiseException('printerType must be a string')
