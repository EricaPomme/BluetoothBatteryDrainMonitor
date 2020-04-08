# BluetoothBatteryDrainMonitor

Tool to record battery levels over time in bluetooth devices in macOS.
## Note:
This is just the absolute barest of bones and more will come later.

## Installation/Usage
1. Clone repo
2. `python3 -m BluetoothBatteryDrainMonitor`

## TODO:
* [!] Implement ordered dicts for returns? It *works* for the AirPods in its current state, but that could easily break.
* Add docstrings
* Expand device detection capabilities (e.g.: mice, other BT headphones, game controllers, etc.)
* Perhaps there's a better way to determine what kind of device we're working with, maybe BT addr ranges? Feature detection?