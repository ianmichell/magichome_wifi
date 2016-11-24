from optparse import OptionParser, OptionGroup
import ast
import time
import random
import socket

from magichome_wifi import MagicHomeLEDController

light = MagicHomeLEDController("192.168.0.92")
try:
    light.connect(False)
    light.update_state()
    print(light.is_on)
    print(light.rgb)
    print(light.brightness)
    print(light.warm_white)
    print(light.cold_white)

except socket.error:
    print(socket.error)
finally:
    light.close()
