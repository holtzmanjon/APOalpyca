from zaber_motion import Units
from zaber_motion.ascii import Connection
from threading import Timer, Lock, Thread
import time
  
class Zaber() :
    def __init__(self, logger=None ) :
        """  Initialize dome properties and capabilities
        """
        self.logger = logger
        self.maxswitch = 1
        self.description = 'Zaber stage'
        self.name = 'Zaber focuser stage'
        self.minvalue = 0
        self.maxvalue = 50000
        self.connected = False
        self.connect()

    def connect(self,port='COM6') :
        self.logger.info('connect Zaber stage')
        self.connection = Connection.open_serial_port(port)
        self.connection.enable_alerts()

        device_list = self.connection.detect_devices()
        self.logger.info("Found {} devices".format(len(device_list)))

        self.device = device_list[0]
        self.axis = self.device.get_axis(1)
        if not self.axis.is_homed():
            self.logger.info('homing axis...')
            self.axis.home()
        self.connected = True

    def home(self) :
        """ Send home asynchronously
        """
        t=Thread(target=self.sendhome)
        t.start()

    def sendhome(self) :
        logger.info('homing axis...')
        self.axis.home()
        logger.info('homed axis...')

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
        """ Move to new position (input in microns) asynchronously
        """
        self.logger.info(f'setting to value: {val}')
        pos=float(val)/1000.
        self.logger.info(f'Moving to {pos}')
        t=Thread(target=lambda : self.move(pos))
        t.start()
        
    def move(self,new_pos,timeout=60000) :
        self.axis.move_absolute(new_pos, Units.LENGTH_MILLIMETRES)
        self.logger.info(f'Moved to {new_pos}')

    def is_moving(self) :
        """ Determine if stage is moving
        """
        p1 = self.get_position()
        time.sleep(0.5)
        p2 = self.get_position()
        if abs(p2-p1)>0.001 : return True
        else : return False

    def get_position(self) :
        """ Return position in microns
        """
        return int(self.axis.get_position(Units.LENGTH_MILLIMETRES)*1000.)

    def get_step(self) :
         return 1
