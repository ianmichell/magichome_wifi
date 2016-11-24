This is a utility for controller MagicHome RGBWWCW Led Lights. Commands were reverse engineered from a RGBWWCW
WIFI controller. Seems to work fine, but... I have only tested this on RGB, so report any bugs in github issues.

I've not ported all the MagicHome app functionality as I don't see any need, given that this is to be used with
home-assistant

##### Functionality available
* Discovery on LAN
* Turning the LED Strips on and off.
* State information
* Setting warm white
* Setting cold white
* Setting RGB Values

##### Not implemented
* Administration and setup of WIFI Controllers. To do this, download the app!
* Remote access administration
* Music related pulsing - Use HUE Emulation in Home Assistant
* Picture / Image based colour changes - See above

##### TODO
* Setting Preset Program
* Setting Custom Program
* Setting Program Speed
* Reading timers
* Setting timers
* Support for other bulbs / controllers