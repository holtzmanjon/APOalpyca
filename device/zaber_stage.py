from zaber_motion import Units
from zaber_motion.ascii import Connection
  
class Zaber() :
    def __init__(self, logger=None ) :
        """  Initialize dome properties and capabilities
        """
        self.maxswitch = 1
        self.description = 'Zaber stage'
        self.name = 'Zaber focuser stage'
        self.minvalue = 0
        self.maxvalue = 50000
        self.connect()

    def connect(self) :
        print('connect Zaber stage')
        self.connection = Connection.open_serial_port(port)
        self.connection.enable_alerts()

        device_list = self.connection.detect_devices()
        print("Found {} devices".format(len(device_list)))

        self.device = device_list[0]
        self.axis = self.device.get_axis(1)
        if not self.axis.is_homed():
            print('homing axis...')
            self.axis.home()
        self.connected = True

    def home(self) :
        self.axis.home()

    def disconnect(self) :
        self.connection.close()
        self.connected=False

    def get_minvalue(self) :
        return self.minvalue

    def get_maxvalue(self) :
        return self.maxvalue

    def get_description(self) :
        return self.description

    def get_name(self) :
        return self.name

    def set_position(self,val) :
        print('setting value',val)
        pos=float(val)/1000.
        self.axis.move_absolute(pos, Units.LENGTH_MILLIMETRES)

    def is_moving(self) :
        return False

    def get_position(self) :
        return int(self.axis.get_position(Units.LENGTH_MILLIMETRES)*1000.)
        return int(self.zaber_stage.get_position()*1000.)

    def get_step(self) :
         return 1
