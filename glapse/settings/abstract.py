from glapse.exception.raiser import Raiser

## a simple abstract/base class
#
# a simple abstract class that provides the methods needed to store and validate a group of settings  
class Abstract(Raiser):
    ## The init does what an init normally does 
    #
    # @param self The object pointer
    # @param input a dict of settings to store and validate
    def __init__(self, input):
        if not isinstance(input, dict):
            self.raiseException('input must be a dict')

        for key in input:
            # set all the settings
            setattr(self, key, input[key])

        self.validate()

    ## returns a copy of the settings  
    #
    # @param self The object pointer
    # @returns a dict containing a copy of the settings 
    def get(self):
        return self.__dict__.copy()

    ## validates the settings  
    #
    # @param self The object pointer
    def validate(self):
        return
