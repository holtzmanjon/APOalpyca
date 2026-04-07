import time

try: 
    from serial import Serial
except: 
    print('no serial')
  
class USBRelay :
    def __init__(self, logger=None, port='COM8' ) :
        """  Initialize relay
        """
        print('init LCUS relay')
        self.maxswitch = 1
        self.description = 'LCUS USB relay'
        self.name = 'USB relay'
        self.minswitchvalue = 0
        self.maxswitchvalue = 1
        self.canasync = False
        self.connect(port=port)

    def connect(self,port='COM7') :
        print('connect LCUS relay')
        self.relay=Serial(port,9600,timeout=1)
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
        start = 0xA0
        address = id+1
        cmd = val
        checksum = start+address+cmd
        self.relay.write(bytes([start,address,cmd,checksum])
        time.sleep(1)

    def getswitch(self,id) :
        return True

    def on_relay(self,id) :
        #self.relay.write(bytes([0xA0, 0x01, 1, 0xA2]))
        self.set_value(id,1) 

    def off_relay(self,id) :
        #self.relay.write(bytes([0xA0, 0x01, 0, 0xA1]))
        self.set_value(id,0) 

