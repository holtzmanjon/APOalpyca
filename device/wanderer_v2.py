import numpy as np

try: 
    from serial import Serial
except: 
    print('no serial')
  
class Wanderer :
    def __init__(self, logger=None ) :
        """  Initialize dome properties and capabilities
        """
        print('init Wanderer')
        self.maxswitch = 3
        self.values = np.zeros(self.maxswitch,dtype=int)
        self.description = 'Wanderer Ultimate Powerbox V2'
        self.name = 'USB3 control'
        self.minswitchvalue = 0
        self.maxswitchvalue = 1
        self.canasync = False
        self.connect(port='COM6')

    def connect(self,port='COM6') :
        print('connect Wanderer')
        self.wanderer=Serial(port,115200,timeout=1)
        self.connected = True

    def connected(self,state) :
        print('connected',state)
        return state

    def canwrite(self,id) :
        return True

    def disconnect(self) :
        self.connected(False)

    def get_description(self,id) :
        return '{:s}, channel {:d}'.format(self.description,id)

    def get_name(self,id) :
        return self.name

    def get_minvalue(self,id) :
        return self.minswitchvalue

    def get_maxvalue(self,id) :
        return self.maxswitchvalue

    def set_value(self,id,val) :
        self.wanderer.write('3{:d}{:d}'.format(id,val).encode())
        self.values[id-1] = val

    def get_value(self,id) :
        return self.values[id-1]

    def getswitch(self,id) :
        return True

    def get_step(self,id) :
        return 1

