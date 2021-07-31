import sys
sys.dont_write_bytecode = True

from settings import printerSettings, miscellaneousSettings, initialCameraSettings, cameraWarmupSettings, cameraSettings, cameraCaptureSettings
from tornado import ioloop
from glapse.settings.printersettings import PrinterSettings
from glapse.settings.miscellaneoussettings import MiscellaneousSettings
from glapse.settings.initialcamerasettings import InitialCameraSettings
from glapse.settings.camerawarmupsettings import CameraWarmupSettings
from glapse.settings.camerasettings import CameraSettings
from glapse.settings.cameracapturesettings import CameraCaptureSettings
from glapse.camera.camera import Camera
from glapse.lapse.controller import Controller
import os, time, traceback

try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    pSettings = PrinterSettings(printerSettings)
    mSettings = MiscellaneousSettings(miscellaneousSettings)
    icSettings = InitialCameraSettings(initialCameraSettings)
    cwSettings = CameraWarmupSettings(cameraWarmupSettings)
    cSettings = CameraSettings(cameraSettings)
    ccSettings = CameraCaptureSettings(cameraCaptureSettings)

    time.sleep(mSettings.wait)

    camera = Camera(icSettings, cwSettings, cSettings, mSettings)
    loop = ioloop.IOLoop.current()
    lapse = Controller(camera, loop, pSettings, mSettings, ccSettings)
    poller = ioloop.PeriodicCallback(callback = lapse.poll, callback_time = mSettings.pollingInterval)
    poller.start()
    loop.start()
except (Exception) as e:
    traceback.print_exc()
    print(e)
except KeyboardInterrupt:
    pass
finally:
    if 'camera' in vars():
        camera.close()

    if 'loop' in vars():
        loop.stop()


    
