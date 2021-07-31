from glapse.exception.raiser import Raiser
import datetime, os

## Handles the communicator between the pi, printer, and pi camera module
#
# The class handled communicating with the printer, as well as ensuring the 
# pi camera module captures images at the appropriate time and stores them in 
# the proper location. 
class Controller(Raiser):
    ## The init does what an init normally does 
    #
    # @param self The object pointer
    # @param camera a glapse.settings.camerasettings.CameraSettings object
    # @param loop a tornado.ioloop.IOLoop object
    # @param printerSettings a glapse.settings.printersettings.PrinterSettings object
    # @param miscellaneousSettings a glapse.settings.miscellaneoussettings.MiscellaneousSettings object
    # @param cameraCaptureSettings a glapse.settings.cameracapturesettings.CameraCaptureSettings object
    # @throws exception various exceptions if picamera fails instantiate   
    def __init__(self, camera, loop, printerSettings, miscellaneousSettings,  cameraCaptureSettings):
        ## @var picamera
        # a picamera object
        self.camera = camera

        ## @var loop
        # a tornado.ioloop.IOLoop object
        self.loop = loop

        ## @var printerSettings
        # a glapse.settings.printersettings.PrinterSettings object
        self.printerSettings = printerSettings

        ## @var miscellaneousSettings
        # a glapse.settings.miscellaneoussettings.MiscellaneousSettings object
        self.miscellaneousSettings = miscellaneousSettings

        ## @var cameraCaptureSettings
        # a glapse.settings.cameracapturesettings.CameraCaptureSettings object
        self.cameraCaptureSettings = cameraCaptureSettings
        
        ## @var ext
        # a str that holds the file extension for captured images 
        self.ext = "." + self.cameraCaptureSettings.format

        ## @var sequence
        # a str that holds the dir path the current sequence of images will be written to 
        self.sequence = None

        ## @var frame
        # a int that holds the current frame/shot number within the current sequence
        self.frame = 0

        ## @var checking
        # a bool that indicates if the printer is currently being polled
        self.checking = False

        ## @var connected
        # a bool that indicates if the printer has been conected to
        self.connected = False

        if self.printerSettings.printerType == 'standAloneDuet':
            from glapse.lapse.interconnects.standaloneduet import StandaloneDuet
            self.interconnect = StandaloneDuet(printerSettings)
        else:
            self.raiseException('only a standalone Duet is currently supported ')

    ## initializes a new sequence
    #
    # The method handles creating a new directory in the proper location on the file system, 
    # as well as updating the appropriate class attributes 
    def initializeSequence(self):
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f")
        dir = os.path.join(self.miscellaneousSettings.capturesDirectory, time)
        oldmask = os.umask(0)
        os.makedirs(dir, 0o777)
        os.umask(oldmask)
        self.sequence = dir
        self.frame = 0

    ## captures a new still image/frame 
    #
    # calls picamera and passes it the appropriate information to capture and write a new 
    # image/frame to the filesystem
    def capture(self):
        if self.sequence is None:
            self.raiseException('gLapse must be initialized before a capture can occur')

        self.frame += 1
        filename = str(self.frame).zfill(6)
        filename = os.path.join(self.sequence, filename + self.ext) 
        self.camera.capture(filename, self.cameraCaptureSettings.get())

    ## performs the grunt work of polling the printer 
    #
    # Handles grunt work of calling the printer, processing responses, and initializing sequences 
    # and calling for image captures based on the responses.
    async def checkForMessages(self):
        if self.checking:
            return
        else:
            self.checking = True

            if self.connected:
                msg = await self.interconnect.checkForMessages()
                if isinstance(msg, str):
                    if msg == 'gLapseInitialize':
                        self.initializeSequence()
                        result = await self.interconnect.resumePrint()
                        if result is False:
                            self.raiseException('failed to resume the print after initialization')

                    if msg == 'gLapseCapture':
                        self.capture() 
                        result = await self.interconnect.resumePrint()
                        if result is False:
                            self.raiseException('failed to resume the print after capture')
            else:
                result = await self.interconnect.connect()
                if result is True:
                    self.connected = True
                else:
                    self.raiseException('failed to connect')

            self.checking = False

    ## a wrapper to catch exceptions 
    #
    # because of how tornado works, a wrapper method must be used to catch exceptions and 
    # terminate the application. 
    async def poll(self):
        try:
            await self.checkForMessages()
        except (Exception) as e:
            print(e)
            self.camera.close()
            self.loop.stop()
            
