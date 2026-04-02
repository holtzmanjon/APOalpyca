try: 
    from serial import Serial
except: 
    print('no serial')
  
class TCube :
    def __init__(self, logger=None ) :
        """  Initialize dome properties and capabilities
        """
        print('init TCube')
        self.maxswitch = 2
        self.description = 'TCube
        self.name = 'CCD cooler'
        self.minswitchvalue = 0
        self.maxswitchvalue = 80
        self.canasync = False
        self.connect(port='COM7')

    def connect(self,port='COM7') :
        print('connect TCube')
        self.tcube=Serial(port,9600,timeout=1)
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
        if val == 1 :
            self.tcube.write('RUN\r'.encode())
        else :
            self.tcube.write('STOP\r'.encode())

    def get_status(self,id) :
        self.tcube.write('GETSET2\r'.format(id+1).encode())
        status = self.tcube.readline()
        print('status: ', status)

    def set_enable(self,id,val) :
        self.tcube.write('EN{:d}={:d}\r'.format(id+1,int(val)).encode())

    def set_dark(self,id,val) :
        self.tcube.write('DARK={:d}\r'.format(int(val)).encode())

    def set_bright(self,id,val) :
        self.tcube.write('BRIGHT={:d}\r'.format(int(val)).encode())

    def getswitch(self,id) :
        return True

    def get_value(self,id) :
        return self.get_tact(id)

    def get_tset(self,id) :
        self.tcube.write('TEMP?\r'.encode())
        print(self.tcube.readline())

    def get_tact(self,id) :
        self.tcube.write('RTD?\r'.encode())
        print(self.tcube.readline())

    def get_step(self,id) :
        return 0.1

