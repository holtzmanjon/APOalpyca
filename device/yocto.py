from yoctopuce.yocto_api import *
from yoctopuce.yocto_temperature import *
from alpaca.camera import *
from threading import Thread
import usbrelay

class Yocto :
    def __init__(self, logger=None,timeout=10,twarn=34,tcrit=37,watchdog=True) :
        """  Initialize dome properties and capabilities
        """
        self.logger=logger
        if self.logger is not None : self.logger.info('init Yocto')
        self.maxswitch = 2
        self.description = 'Yocto thermocouple'
        self.name = 'Yocto thermocouple'
        self.canasync = False
        self.connected = False
        self.timeout = timeout
        self.twarn = twarn
        self.tcrit = tcrit
        if watchdog : self.start_watchdog()
        self.connect()

    def connect(self) :
        if self.logger is not None : self.logger.info('connect Yocto')
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
        self.watchdog=Thread(target=self.reset_watchdog)
        self.watchdog.start()

    def stop_watchdog(self) :
        """ Stop watchdog thread
        """        
        if self.watchdog is not None : self.watchdog.stop()

    def ccd_power(self) :
        """ Toggle relay once to turn camera power on (until hardware watchdog turns it off!)
        """
        relay=usbrelay.USBRelay()
        relay.on_relay(1)
        time.sleep(1)
        relay.off_relay(1)
    
    def reset_watchdog(self) :
        """ Reset watchdog periodically
        """
        self.ccd_power()
        print('connect camera in ASCOM Remote now (10s)!')
        time.sleep(10)
        C = Camera("172.24.4.202:11111",0)
        relay=usbrelay.USBRelay()

        while True :
            tccd=-999
            tset=-999
            power=-999
            try : 
                tccd = C.CCDTemperature
                tset = C.SetCCDTemperature
                power = C.CoolerPower
            except :
                self.logger.info("error reading CCD values")
                print("error reading CCD values")
                pass

            t1 = self.get_value(0)
            t2 = self.get_value(1)
            if self.logger is not None :self.logger.info('tccd: {:f} {:f} {:f} thermocouple: {:f} {:f}'.format(tccd,tset,power,t1,t2))
            print('tccd: {:f} {:f} {:f} thermocouple: {:f} {:f}'.format(tccd,tset,power,t1,t2))
            if t1 > self.twarn or t2 > self.twarn :
                #if temp > twarn, turn off cooler power, but not camera, and stay in loop
                if self.logger is not None : self.logger.info('turning off cooler...')
                C.CoolerOn = False
            if t1 < self.tcrit and t2 < self.tcrit :
                # if temp<tcrit, reset watchdog to keep camera on
                if self.logger is not None : self.logger.info('resetting watchdog...')
                relay.on_relay(1)
                time.sleep(1)
                relay.off_relay(1)
            else :
                # let camera go off and exit loop
                if self.logger is not None : self.logger.info('temp out of range, break...')
                break

            time.sleep(self.timeout)


