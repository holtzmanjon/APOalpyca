"""
lts_pythonnet
==================

An example of using the LTS integrated stages with python via pythonnet

Implement ASCOM calls
"""
import time
import clr
from threading import Timer, Lock, Thread

try :
    clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
    clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
    clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.IntegratedStepperMotorsCLI.dll")
    from Thorlabs.MotionControl.DeviceManagerCLI import *
    from Thorlabs.MotionControl.GenericMotorCLI import *
    from Thorlabs.MotionControl.IntegratedStepperMotorsCLI import *
    from System import Decimal  # necessary for real world units
except :
    print('no Thorlabs')

class LTS150 :
    def __init__(self,logger=None,serial_no="45441684",name='iodine stage') :
        """  Initialize dome properties and capabilities
        """
        self.logger = logger
        self.maxswitch = 1
        self.description = 'Thorlabs LTS 150'
        self.serial_no = serial_no
        self.name = name
        self.minswitchvalue = 0*1000
        self.maxswitchvalue = 150*1000
        self.connected = False
        t=Thread(target=self.connect)
        t.start()

    def connect(self) :
        self.logger.info('connect LTS 150')
        DeviceManagerCLI.BuildDeviceList()
        # create new device
        # Connect, begin polling, and enable
        self.device = LongTravelStage.CreateLongTravelStage(self.serial_no)
        self.device.Connect(self.serial_no)

        # Ensure that the device settings have been initialized
        if not self.device.IsSettingsInitialized():
            self.device.WaitForSettingsInitialized(10000)  # 10 second timeout
            assert self.device.IsSettingsInitialized() is True

        # Start polling and enable
        self.device.StartPolling(250)  #250ms polling rate
        time.sleep(5)
        self.device.EnableDevice()
        time.sleep(0.25)  # Wait for device to enable

        # Get Device Information and display description
        self.device_info = self.device.GetDeviceInfo()
        self.logger.info(self.device_info.Description)

        # Load any configuration settings needed by the controller/stage
        motor_config = self.device.LoadMotorConfiguration(self.serial_no)

        # Get parameters related to homing/zeroing/other
        home_params = self.device.GetHomingParams()
        self.logger.info(f'Homing velocity: {home_params.Velocity}')
        self.logger.info(f'Homing Direction: {home_params.Direction}')
        home_params.Velocity = Decimal(10.0)  # real units, mm/s
        # Set homing params (if changed)
        self.device.SetHomingParams(home_params)
        self.logger.info('connected LTS 150')
        self.connected = True

    def disconnect(self) :
        self.device.StopPolling()
        self.device.Disconnect()
        self.connected=False

    def get_description(self) :
        return self.description

    def get_name(self) :
        return self.name

    def get_minvalue(self) :
        return self.minswitchvalue

    def get_maxvalue(self) :
        return self.maxswitchvalue

    def set_position(self,val) :
        """ Set position to val in microns
        """
        position=float(val/1000.)
        # Move the device to a new position
        new_pos = Decimal(position)  # Must be a .NET decimal
        self.logger.info(f'Moving to {position}')
        t=Thread(target=lambda : self.move(new_pos))
        t.start()

    def move(self,new_pos,timeout=60000) :
        self.device.MoveTo(new_pos, timeout)  # 60 second timeout

    def getswitch(self) :
        return True

    def get_position(self) :
        """ Return position in microns
        """
        return Decimal.ToInt32(self.device.get_Position()*Decimal(1000))

    def get_step(self) :
         return 1

    def home(self) :
        t=Thread(target=self.sendhome)
        t.start()

    def sendhome(self) :
        # Home or Zero the device (if a motor/piezo)
        self.logger.info("Homing Device")
        self.device.Home(60000)  # 60 second timeout
        self.logger.info("Done")

    def get_velocity(self) :
        return Decimal.ToDouble(self.device.get_Velocity())

    def set_velocity(self,velocity) :
        # Get Velocity Params
        vel_params = self.device.GetVelocityParams()
        vel_params.MaxVelocity = Decimal(50.0)  # This is a bad idea
        self.device.SetVelocityParams(vel_params)

    def is_moving(self) :
        p1 = self.get_position()
        time.sleep(0.5)
        p2 = self.get_position()
        if abs(p2-p1)>0.001 : return True
        else : return False
