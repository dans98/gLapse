from glapse.settings.abstract import Abstract

## stores and validates picamera settings that are set after 
# the camera has been given time to warm-up
class CameraWarmupSettings(Abstract):
    ## The init does what an init normally does 
    #
    # @param self The object pointer
    # @param input a dict of settings to store and validate
    def __init__(self, input):
        super(CameraWarmupSettings,self).__init__(input)
