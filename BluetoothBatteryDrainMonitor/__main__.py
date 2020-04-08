from BluetoothBatteryDrainMonitor import *
import plistlib
import argparse
import csv
import os
import sys

from pprint import pprint


def setup() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', type=str, nargs='?', help='BT address of device to record. Leave blank for a list of devices.')
    parser.add_argument('-path', type=str, default='/Library/Preferences/com.apple.Bluetooth.plist', help='Location of bluetooth plist')
    parser.add_argument('-interval', type=int, default=5, help='Sampling interval, in seconds (default: 5)')
    return parser.parse_args()

def params_present(device: dict, params: tuple) -> bool:
    if type(params) is not tuple:
        raise ValueError(f"Expected tuple, got {type(params)}. If only checking a single item, make sure you have a comma after the tuple entry.  (e.g: \"(\'Name\',)\"  ).'")
    return all([i in device.keys() for i in params])

def update_device_list() -> list:
    global args
    devices = []
    with open(args.path, 'rb') as fd:
        plist = plistlib.load(fd)['DeviceCache']
        for device in plist:
            # TODO: Add regex check to make sure we're not trying to parse anything that's not keyed as a BT addr
            this_device = plist[device]
            this_device.update(addr=device)
            
            # Attempt to determine what kind of device we're looking at based on the parameters in the plist dict
            # Specific classes for each type of device are located in devices.py
            # TODO: Expand device detection capabilities (e.g.: mice, other BT headphones, game controllers, etc.)
            # TODO: Perhaps there's a better way to determine what kind of device we're working with, maybe BT addr ranges? Feature detection?            
            if params_present(this_device, ('BatteryPercentCase', 'BatteryPercentLeft', 'BatteryPercentRight')):
                devices.append(AirPods(this_device))
            else:
                devices.append(Device(this_device))
    return devices

if __name__ == '__main__':
    args = setup()
    print(args)
    if not args.addr:
        for device in sorted(update_device_list(), key=lambda x: x.name):
            print(f"{device.addr}: {device.name}")