from glapse.settings.abstract import Abstract
import os

## stores and validates picamera settings used during the capture of still images/frames
class CameraCaptureSettings(Abstract):
    ## The init does what an init normally does 
    #
    # @param self The object pointer
    # @param input a dict of settings to store and validate
    def __init__(self, input):
        super(CameraCaptureSettings,self).__init__(input)

    ## validates the settings  
    #
    # @param self The object pointer
    # @throws exception id a setting fails validation 
    def validate(self):
        if not hasattr(self, 'format'):
            self.raiseException('format is a required setting')

        if not isinstance(self.format, str):
            self.raiseException('format must be a string')
            