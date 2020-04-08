import argparse
import csv
import plistlib
import sys
import time
import os

from BluetoothBatteryDrainMonitor import *


def setup() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', type=str, nargs='?', help='BT address of device to record. Leave blank for a list of devices.')
    parser.add_argument('-path', type=str, default='/Library/Preferences/com.apple.Bluetooth.plist', help='Location of bluetooth plist')
    parser.add_argument('-interval', type=float, default=5, help='Sampling interval, in seconds (default: 5)')
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

            # AirPods (Tested with gen 1 AirPods)
            if params_present(this_device, ('BatteryPercentCase', 'BatteryPercentLeft', 'BatteryPercentRight')):
                devices.append(AirPods(this_device))
            # Unknown devices get a generic Device that's just their address, name, and the full output from the plist.
            else:
                devices.append(Device(this_device))
    return devices

def write_log(device, log_file: str) -> None:
    keys = sorted(device.levels().keys())
    header = ['elapsed']
    header += keys
    row = [time.perf_counter()]
    for key in keys:
        row.append(device.levels()[key])
    if not os.path.exists(log_file):
        with open(log_file, 'w', encoding='utf-8') as fd:
            csv.writer(fd, quoting=csv.QUOTE_ALL).writerow(header)
    with open(log_file, 'a', encoding='utf-8') as fd:
        csv.writer(fd, quoting=csv.QUOTE_ALL).writerow(row)

if __name__ == '__main__':
    args = setup() 
    start_timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    if not args.addr:
        for device in sorted(update_device_list(), key=lambda x: x.name):
            print(f"{device.addr}: {device.name}")
    else:
        while True:
            try:
                for device in update_device_list():
                    if device.addr == args.addr:
                        status_msg = ', '.join([f"{k}: {v}" for k, v in device.levels().items()])
                        print(f"{device.name} ({device.addr}): {status_msg}")
                        write_log(device, f"{args.addr}__{start_timestamp}.csv")
                time.sleep(args.interval)
            except KeyboardInterrupt:
                break
        