from optparse import OptionParser, OptionGroup
import ast
import time

from magichome_wifi import MagicHomeLEDController

light = MagicHomeLEDController("192.168.0.92")
try:
    light.connect()
    light.turn_on()
    light.set_rgb([255, 0, 0])
    time.sleep(2)
finally:
    light.turn_off()
    light.close()
