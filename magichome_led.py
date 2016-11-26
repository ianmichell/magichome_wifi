"""
Support for Generic MagicHome Controllers with RGB WW CW
TODO Add white and cold white support
"""
import logging
import socket
import random

import voluptuous as vol

from homeassistant.const import CONF_DEVICES, CONF_NAME
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, ATTR_RGB_COLOR, ATTR_EFFECT, EFFECT_RANDOM,
    SUPPORT_BRIGHTNESS, SUPPORT_EFFECT, SUPPORT_RGB_COLOR, Light,
    PLATFORM_SCHEMA)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['https://github.com/thunderbird/magichome_wifi/archive/0.1.zip'
                '#magichome_wifi==0.1']

_LOGGER = logging.getLogger(__name__)

CONF_AUTOMATIC_ADD = 'automatic_add'
ATTR_MODE = 'mode'
ATTR_WARM_WHITE = 'warm_white'
ATTR_COLD_WHITE = 'cold_white'

DOMAIN = 'magichome_led'

SUPPORT_MAGICHOME_LED = (SUPPORT_BRIGHTNESS | SUPPORT_EFFECT |
                    SUPPORT_RGB_COLOR)

DEVICE_SCHEMA = vol.Schema({
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(ATTR_MODE, default='rgbwwcw'):
        vol.All(cv.string, vol.In(['rgbwwcw', 'rgbww', 'rgb'])),
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_DEVICES, default={}): {cv.string: DEVICE_SCHEMA},
    vol.Optional(CONF_AUTOMATIC_ADD, default=False):  cv.boolean,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Magichome Lights."""
    import magichome_wifi
    lights = []
    light_ips = []
    for ipaddr, device_config in config[CONF_DEVICES].items():
        device = {}
        device['name'] = device_config[CONF_NAME]
        device['ip'] = ipaddr
        # TODO: Add more options here... We want to allow different channels
        device[ATTR_MODE] = device_config[ATTR_MODE]
        light = MagicHomeLight(device)
        if light.is_valid:
            lights.append(light)
            light_ips.append(ipaddr)

    if not config[CONF_AUTOMATIC_ADD]:
        add_devices(lights)
        return

    # Find the bulbs / controllers on the LAN
    _LOGGER.info("Scanning for MagicHomeLED Controllers")
    response = magichome_wifi.MagicHomeLEDController.scan(timeout=10)
    for device in response:
        _LOGGER.info("Found: " + device)
        ipaddr = device['ip']
        if ipaddr in light_ips:
            continue
        device['name'] = device['mac'] + " " + ipaddr
        device[ATTR_MODE] = 'rgbwwcw'
        light = MagicHomeLight(device)
        if light.is_valid:
            lights.append(light)
            light_ips.append(ipaddr)

    add_devices(lights)

class MagicHomeLight(Light):
    """Representation of a MagicHome Light."""

    def __init__(self, device):
        """Initialize MagicHome WIFI."""
        import magichome_wifi

        self._name = device['name']
        self._ipaddr = device['ip']
        self._mode = device[ATTR_MODE]
        self.is_valid = True

        try:
            self._bulb = magichome_wifi.MagicHomeLEDController(ip=self._ipaddr)
            _LOGGER.info("Connecting to bulb: " + self._name + "IP: " + self._ipaddr)
            self._bulb.connect()
            _LOGGER.info("Connected to bulb: " + self._name)
        except socket.error:
            self.is_valid = False
            _LOGGER.error(
                "Failed to connect to bulb %s, %s", self._ipaddr, self._name)

    @property
    def unique_id(self):
        """Return the ID of this light."""
        return "{}.{}".format(self.__class__, self._ipaddr)

    @property
    def name(self):
        """Return the name of the device if any."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._bulb.is_on

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        return self._bulb.brightness

    @property
    def rgb_color(self):
        """Return the color property."""
        return self._bulb.rgb

    @property
    def white_value(self):
        return self._bulb.warm_white

    @property
    def coldwhite_value(self):
        return self._bulb.cold_white

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_MAGICHOME_LED

    def turn_on(self, **kwargs):
        """Turn the specified or all lights on."""
        try:
            if not self.is_on:
                self._bulb.turn_on()

            rgb = kwargs.get(ATTR_RGB_COLOR)
            brightness = kwargs.get(ATTR_BRIGHTNESS)
            effect = kwargs.get(ATTR_EFFECT)
            if rgb is not None and brightness is not None:
                self._bulb.set_rgb(rgb, 0, 0, brightness)
            elif rgb is not None:
                self._bulb.set_rgb(rgb)
            elif brightness is not None:
                    self._bulb.set_brightness(brightness)
            elif effect == EFFECT_RANDOM:
                self._bulb.set_rgb([random.randrange(0, 255),
                                  random.randrange(0, 255),
                                  random.randrange(0, 255)])
        except socket.error:
            self._bulb.close()
            self._bulb.connect()

    def turn_off(self, **kwargs):
        """Turn the specified or all lights off."""
        self._bulb.turn_off()

    def update(self):
        """Synchronize state with bulb."""
        _LOGGER.info("Updating bulb state: " + self._name)
        self._bulb.update_state()
