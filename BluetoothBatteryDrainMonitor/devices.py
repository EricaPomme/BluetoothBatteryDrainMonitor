import unicodedata

class Device(object):
    def __init__(self, *args) -> None:
        # The only argument we should be getting is a dict from the plist. If we don't, throw a ValueError
        if type(args[0]) is not dict:
            raise ValueError(f"Expected dict, got {type(args[0])}")
        else:
            self.attribs = args[0]

        self.addr = self.attribs['addr']
        
        if 'displayName' in self.attribs.keys():
            self.name = unicodedata.normalize('NFKD', self.attribs['displayName'])
        elif 'Name' in self.attribs.keys():
            self.name = unicodedata.normalize('NFKD', self.attribs['Name'])
        else:
            self.name = 'Unknown'
        
        # Blacklist of attributes to ignore when returning values from certain class methods, name and addr by default.
        self.blacklist = (
            'name',
            'addr'
        )

    def levels(self) -> dict:
        # This method will be overwritten by functions in each class for known devices
        # For now, just return a dict of any potentially changing parameters (e.g.: Everything but name and address.)
        return {k:v for k,v in self.attribs.items() if k not in self.blacklist}
    
    def attrib_keys(self) -> list:
        return [k for k in self.attribs.keys() if k not in self.blacklist]

class AirPods(Device):
    def __init__(self, *args):
        super().__init__(*args)
        self.case = args[0]['BatteryPercentCase']
        self.left = args[0]['BatteryPercentLeft']
        self.right = args[0]['BatteryPercentRight']
        
    def levels(self) -> dict:
        return {
            'case': self.case,
            'left': self.left,
            'right': self.right
        }

    # TODO: Make this and any other device specific entries more pythonic    
    def attrib_keys(self) -> list:
        return [
            'case',
            'left',
            'right'
        ]