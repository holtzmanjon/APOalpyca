try: 
    from serial import Serial
except: 
    print('no serial')
  
class TCube :
    def __init__(self, logger=None, port='COM8',baudrate=9600 ) :
        """  Initialize dome properties and capabilities
        """
        print('init TCube')
        self.maxswitch = 2
        self.description = 'TCube'
        self.name = 'CCD cooler'
        self.minswitchvalue = 0
        self.maxswitchvalue = 80
        self.canasync = False
        self.connect(port=port,baudrate=baudrate)

    def connect(self,port='COM7',baudrate=9600) :
        print('connect TCube')
        self.tcube=Serial(port,baudrate,timeout=1)
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

    def read_status(self,status) :
        out=status.decode().split('\r')
        self.temp=float(out[0])
        self.settemp=float(out[1])
        self.pumptemp=float(out[2])
        self.pwm=float(out[3])
        self.fanpwm=float(out[4])
        self.tll=out[5]
        self.stat1a=int(out[6])
        self.flt1a=int(out[7])

    def status(self,id) :
        self.tcube.write('GETSET2\r'.format(id+1).encode())
        status = self.tcube.readline()
        self.read_status(status)
        print('status: ', status)
        print('temp: ', self.temp)
        print('settemp: ', self.settemp)
        print('pumptemp: ', self.pumptemp)
        print('pwm: ', self.pwm)
        print('fanpwm: ', self.fanpwm)
        print('tll: ', self.tll)
        print('stat1a: ', bin(self.stat1a))
        print('flt1a: ', bin(self.flt1a))

    def getswitch(self,id) :
        return True

    def get_value(self,id) :
        return self.get_tact(id)

    def get_tset(self,id) :
        self.tcube.write('SETTEMP?\r'.encode())
        return self.tcube.readline()

    def get_tact(self,id) :
        self.tcube.write('TEMP?\r'.encode())
        return self.tcube.readline()
  
    def tset(self,id,val) :
        self.tcube.write('TEMP {:f}\r'.format(val).encode())
        return self.get_tset(id)

    def get_step(self,id) :
        return 0.1

    def write(self,command) :
        self.tcube.write((command+'\r').encode())

    def read(self) :
        out=self.tcube.readline()
        print(out)

