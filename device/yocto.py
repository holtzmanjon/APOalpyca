from yoctopuce.yocto_api import *
from yoctopuce.yocto_temperature import *
from alpyca.camera import *

class Yocto :
    def __init__(self, logger=None ) :
        """  Initialize dome properties and capabilities
        """
        self.logger=logger
        self.logger.info('init Yocto')
        self.maxswitch = 2
        self.description = 'Yocto thermocouple'
        self.name = 'Yocto thermocouple'
        self.canasync = False
        self.connected = False
        self.start_watchdog()
        self.connect()

    def connect(self) :
        self.logger.info('connect Yocto')
        errmsg=YRefParam()
        YAPI.RegisterHub("usb",errmsg)
        self.temp=[YTemperature.FindTemperature(f"THRMCPL1-286EEC.temperature1"),
                   YTemperature.FindTemperature(f"THRMCPL1-286EEC.temperature2")]
        self.connected = True

    def connected(self,state) :
        return state

    def canwrite(self,id) :
        return False

    def disconnect(self) :
        self.connected(False)

    def get_description(self,id) :
        return '{:s}, channel {:d}'.format(self.description,id)

    def get_name(self,id) :
        return self.name

    def getswitch(self,id) :
        return True

    def get_value(self,id) :
        return self.temp[id].get_currentValue()

    def get_step(self,id) :
        return 0.1

    def start_watchdog(self) :
        """ Start thread to periodically reset watchdog
        """
        t=Thread(target=self.reset_watchdog)
        t.start()
    
    def reset_watchdog(self,timeout=110) :
        """ Reset watchdog periodically
        """
        #C = Camera("localhost:11111",0)
        relay=usbrelay.USBRelay()

        while True :
            #tccd = C.CCDTemperature
            t1 = self.get_value(0)
            t2 = self.get_value(1)
            logger.info('tccd: {:f} {:f} {:f} thermocouple: {:f} {:f}'.format(tccd,C.SetCCDTemperature,C.CoolerPower,t1,t2))
            if t1 < 30 and t2 < 30 :
                # reset watchdog
                logger.info('resetting watchdog...')
                relay.on_relay(1)
                time.sleep(1)
                relay.off_relay(1)

            time.sleep(10)


