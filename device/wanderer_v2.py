import numpy as np
import time

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
        self.wanderer=Serial(port,19200,timeout=1)
        time.sleep(2)
        self.connected = True
        # start with all ports on
        for id in range(self.maxswitch) :
            self.set_value(id,1)

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
        print('sending: ','3{:d}{:d}'.format(id+1,int(val)))
        self.wanderer.write('3{:d}{:d}'.format(id+1,int(val)).encode())
        self.values[id] = val

    def get_value(self,id) :
        return self.values[id]

    def getswitch(self,id) :
        return True

    def get_step(self,id) :
        return 1

