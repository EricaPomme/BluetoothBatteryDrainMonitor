import unicodedata

class Device(object):
    def __init__(self, *args):
        # The only argument we should be getting is a dict from the plist. If we don't, throw a ValueError
        if type(args[0]) is not dict:
            raise ValueError(f"Expected dict, got {type(args[0])}")
        
        self.addr = args[0]['addr']
        
        if 'displayName' in args[0].keys():
            self.name = unicodedata.normalize('NFKD', args[0]['displayName'])
        elif 'Name' in args[0].keys():
            self.name = unicodedata.normalize('NFKD', args[0]['Name'])
        else:
            self.name = 'Unknown'




class AirPods(Device):
    def __init__(self, *args):
        super().__init__(*args)


# dev_id: str, case_level: int, left_level: int, right_level: int