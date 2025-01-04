from serial import Serial
  
class TC300() :
    def __init__(self, logger=None ) :
        """  Initialize dome properties and capabilities
        """
        print('init TC300')
        self.maxswitch = 2
        self.description = 'Thorlabs TC 300'
        self.name = 'Iodine temperature'
        self.minswitchvalue = 0
        self.maxswitchvalue = 80
        self.canasync = False
        self.connect(port='COM7')

    def connect(self,port='COM7') :
        print('connect TC300')
        self.tc300=Serial(port,115200,timeout=1)
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
        self.tc300.write('TSET{:d}={:d}\r'.format(id+1,int(val*10)).encode())
        self.tc300.readline()
        self.tc300.write('EN{:d}=1\r'.format(id+1).encode())
        self.tc300.readline()

    def get_enable(self,id) :
        self.tc300.write('EN{:d}?\r'.format(id+1).encode())
        return int(self.tc300.readline().strip(b'>').split()[0])

    def set_enable(self,id,val) :
        self.tc300.write('EN{:d}={:d}\r'.format(id+1,int(val)).encode())
        self.tc300.readline()

    def getswitch(self,id) :
        return True

    def get_value(self,id) :
        return self.get_tact(id)

    def get_tset(self,id) :
        self.tc300.write('TSET{:d}?\r'.format(id+1).encode())
        return float(self.tc300.readline().strip(b'>').split()[0])

    def get_tact(self,id) :
        self.tc300.write('TACT{:d}?\r'.format(id+1).encode())
        return float(self.tc300.readline().strip(b'>').split()[0])

    def get_voltage(self,id) :
        self.tc300.write('VOLT{:d}?\r'.format(id+1).encode())
        return float(self.tc300.readline().strip(b'>').split()[0])

    def get_current(self,id) :
        self.tc300.write('CURR{:d}?\r'.format(id+1).encode())
        return float(self.tc300.readline().strip(b'>').split()[0])

    def get_step(self,id) :
         return 0.1

