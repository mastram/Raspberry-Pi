## Install GPS Utilities
`sudo apt-get install gpsd gpsd-clients python-gps`

## To auto start GPSD Demon

Default settings for the gpsd init script and the hotplug wrapper.
This is done in the file : /etc/default/gpsd

Start the gpsd daemon automatically at boot time
`START_DAEMON="true"`

Use USB hotplugging to add new USB devices automatically to the daemon
`USBAUTO="true"`

Devices gpsd should collect to at boot time.
They need to be read/writeable, either by user gpsd or the group dialout.
`DEVICES="/dev/ttyUSB0"`

Other options you want to pass to gpsd
`GPSD_OPTIONS="-F /var/run/gpsd.sock -b -n"`

## Restart the service
`sudo /etc/init.d/gpsd restart`

## Test
`cgps -s`
