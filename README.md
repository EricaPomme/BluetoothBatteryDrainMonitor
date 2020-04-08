# BluetoothBatteryDrainMonitor

Tool to record battery levels over time in bluetooth devices in macOS.

## Installation/Usage
1. Clone repo
2. `python3 -m BluetoothBatteryDrainMonitor`
    * If you know the address you want to monitor, specify it as a positional argument. (Example: `python3 -m BluetoothBatteryMonitor a1-b2-c3-d4-e5-f6`)
    * If you don't know the address of the device you want to monitor, running with no arguments will print a list of devices in the DeviceCache and exit.
        * If the device you want isn't listed, make sure it's paired with the system and you can use it.

### Supported arguments
* `-h`, `--help` to print help.
* `-plist [path]` Path to your bluetooth plist. This defaults to `/Library/Preferences/com.apple.Bluetooth.plist`, and is unlikely to be different on your system.
* `-interval [seconds]` Set the delay between samples. Defaults to 5 seconds.

## TODO:
* Add docstrings
* Expand device detection capabilities (e.g.: mice, other BT headphones, game controllers, etc.)
* Perhaps there's a better way to determine what kind of device we're working with, maybe BT addr ranges? Feature detection?
* Allow for logging multiple devices at once