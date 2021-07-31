from picamera import PiCamera
import time

## Handles interaction with the picamera class 
#
# The class is designed to encapsulate picamera and handle all interactions with it.
# such as instantiating, configuring, closing, capturing images, and capturing video
class Camera:
    ## The init instantiates picamera
    #
    # @param self The object pointer
    # @param initialCameraSettings a glapse.settings.initialcamerasettings.InitialCameraSettings object
    # @param cameraWarmupSettings a glapse.settings.camerawarmupsettings.CameraWarmupSettings object
    # @param cameraSettings a glapse.settings.camerasettings.CameraSettings object
    # @param miscellaneousSettings a glapse.settings.miscellaneoussettings.MiscellaneousSettings object
    # @throws exception various exceptions if picamera fails instantiate   
    def __init__(self, initialCameraSettings, cameraWarmupSettings, cameraSettings, miscellaneousSettings):
        ## @var picamera
        # The picamera object
        self.camera = PiCamera(**initialCameraSettings.get())

        ## @var boolean
        # has picamera been instantiated
        self.instantiated = True

        settings = cameraWarmupSettings.get()
        for key in settings:
            # set all the normal settings
            setattr(self.camera, key, settings[key])

        time.sleep(miscellaneousSettings.cameraWarmup)

        settings = cameraSettings.get()
        for key in settings:
            # set all the normal settings
            setattr(self.camera, key, settings[key])

    ## closes picamera
    #
    # @param self The object pointer
    def close(self):
        if self.instantiated:
            self.camera.close()
            self.instantiated = False
      
    ## makes picamera capture an image
    #
    # @param self The object pointer
    # @param filename the full name and path of the image to be captured
    # @param captureSettings a dict of settings that will be used when capturing the image
    def capture(self, filename, captureSettings):
        if self.instantiated:
            self.camera.capture(filename, **captureSettings)