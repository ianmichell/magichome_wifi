from optparse import OptionParser, OptionGroup
import ast
import time
import random
import socket

from magichome_wifi import MagicHomeLEDController

light = MagicHomeLEDController("192.168.0.92")
try:
    light.connect(False)
    light.update_state(False)
    assert not light.is_on
    light.turn_on()
    light.update_state(False)
    assert light.is_on
    light.set_rgb(["255", "255", "0"])
    light.set_rgb([random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)])
    time.sleep(2)
except socket.error:
    print(socket.error)
finally:
    light.turn_off()
    light.close()
