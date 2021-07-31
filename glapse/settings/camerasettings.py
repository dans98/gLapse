from glapse.settings.abstract import Abstract

## stores and validates picamera settings set immediately after the camera 
# object has been instantiated 
class CameraSettings(Abstract):
    ## The init does what an init normally does 
    #
    # @param self The object pointer
    # @param input a dict of settings to store and validate
    def __init__(self, input):
        super(CameraSettings,self).__init__(input)
