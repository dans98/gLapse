from glapse.settings.abstract import Abstract
import os

## stores and validates general settings for the application
class MiscellaneousSettings(Abstract):
    ## The init does what an init normally does 
    #
    # @param self The object pointer
    # @param input a dict of settings to store and validate
    def __init__(self, input):
        super(MiscellaneousSettings,self).__init__(input)

    ## validates the settings  
    #
    # @param self The object pointer
    # @throws exception id a setting fails validation 
    def validate(self):
        if not hasattr(self, 'capturesDirectory'):
            self.raiseException('capturesDirectory is a required setting')

        if not hasattr(self, 'pollingInterval'):
            self.raiseException('pollingInterval is a required setting')

        if not hasattr(self, 'wait'):
            self.raiseException('wait is a required setting')

        if not hasattr(self, 'cameraWarmup'):
            self.raiseException('cameraWarmup is a required setting')

        if not isinstance(self.capturesDirectory, str):
            self.raiseException('capturesDirectory must be a string')

        if not os.access(self.capturesDirectory, os.F_OK):
            self.raiseException('captureDirectory does not exist')

        if not os.access(self.capturesDirectory, os.W_OK):
            self.raiseException('captureDirectory cannot be written to')

        if not isinstance(self.pollingInterval, int):
            self.raiseException('pollingInterval must be a integer')

        if not isinstance(self.wait, int):
            self.raiseException('wait must be a integer')

        if not isinstance(self.cameraWarmup, int):
            self.raiseException('cameraWarmup must be a integer')
