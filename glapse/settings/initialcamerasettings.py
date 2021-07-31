from glapse.settings.abstract import Abstract

## stores and validates picamera settings needed to instantiate the camera object
class InitialCameraSettings(Abstract):
    ## The init does what an init normally does 
    #
    # @param self The object pointer
    # @param input a dict of settings to store and validate
    def __init__(self, input):
        super(InitialCameraSettings,self).__init__(input)
