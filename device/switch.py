
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# switch.py - Alpaca API responders for Switch
#
# Author:   Jon Holtzman < holtz@nmsu.edu >
#
# -----------------------------------------------------------------------------
# Edit History:
#   Generated by Python Interface Generator for AlpycaDevice
#
# 27-Dec-2024   Initial edit

from falcon import Request, Response, HTTPBadRequest, before
from logging import Logger
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \
                StateValue, get_request_field, to_bool
from exceptions import *        # Nothing but exception classes

logger: Logger = None

from tc300 import TC300
from lts150 import LTS150

# ----------------------
# MULTI-INSTANCE SUPPORT
# ----------------------
# If this is > 0 then it means that multiple devices of this type are supported.
# Each responder on_get() and on_put() is called with a devnum parameter to indicate
# which instance of the device (0-based) is being called by the client. Leave this
# set to 0 for the simple case of controlling only one instance of this device type.
#
maxdev = 1                      # Single instance

# -----------
# DEVICE INFO
# -----------
# Static metadata not subject to configuration changes
class Switch0Metadata:
    """ Metadata describing the Switch Device. Edit for your device"""
    Name = 'Thorlabs TC300 Temperature controller'
    Version = '1.0.0'
    Description = 'LTS Temperature controller'
    DeviceType = 'Switch'
    DeviceID = 'e32cca17-899f-401a-bb50-596db7f9a3ee'
    Info = 'Alpaca Sample Device\nImplements ISwitch\nASCOM Initiative'
    MaxDeviceNumber = maxdev
    InterfaceVersion = 3

class Switch1Metadata:
    """ Metadata describing the Switch Device. Edit for your device"""
    Name = 'Thorlabs LTS Stage'
    Version = '1.0.0'
    Description = 'LTS Stage'
    DeviceType = 'Switch'
    DeviceID = '75a88d87-15da-4d2f-94ba-612cd5bb0fea'
    Info = 'Alpaca Sample Device\nImplements ISwitch\nASCOM Initiative'
    MaxDeviceNumber = maxdev
    InterfaceVersion = 3

switch_dev = None
def start_switch_device(logger: logger):
    logger = logger
    global switch_dev
    switch_dev = [TC300(logger=logger),LTS150(logger=logger)]

# --------------------
# RESOURCE CONTROLLERS
# --------------------

@before(PreProcessRequest(maxdev))
class action:
    def on_put(self, req: Request, resp: Response, devnum: int):
        if devnum == 0 :
            idstr = get_request_field('Parameters', req)      # Raises 400 bad request if missing
            try:
                id = int(idstr)
            except:
                resp.text = MethodResponse(req,
                                InvalidValueException(f'Id {idstr} not a valid integer.')).json
                return
            if id < 0 or id > switch_dev[devnum].maxswitch -1 :
                resp.text = MethodResponse(req,
                                InvalidValueException(f'Id " + idstr + " not in range.')).json
                return
            try:
                if req.get_media()['Action'] == 'get_tset' :
                    val = switch_dev[devnum].get_tset(id)
                elif req.get_media()['Action'] == 'get_voltage' :
                    val = switch_dev[devnum].get_voltage(id)
                elif req.get_media()['Action'] == 'get_current' :
                    val = switch_dev[devnum].get_current(id)
                resp.text = PropertyResponse(val, req).json
            except Exception as ex:
                resp.text = PropertyResponse(None, req,
                    DriverException(0x500, 'Switch.Action failed', ex)).json
        else :
            resp.text = MethodResponse(req, NotImplementedException()).json


@before(PreProcessRequest(maxdev))
class commandblind:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandbool:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandstring:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class connect:
    def on_put(self, req: Request, resp: Response, devnum: int):
        try:
            # ------------------------
            ### CONNECT THE DEVICE ###
            switch_dev[devnum].connect()
            # ------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Connect failed', ex)).json

@before(PreProcessRequest(maxdev))
class connected:
    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # -------------------------------------
            is_conn = switch_dev[devnum].connected ### READ CONN STATE ###
            # -------------------------------------
            resp.text = PropertyResponse(is_conn, req).json
        except Exception as ex:
            resp.text = MethodResponse(req, DriverException(0x500, 'Switch.Connected failed', ex)).json

@before(PreProcessRequest(maxdev))
class connecting:
    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # ------------------------------
            val = switch_dev[devnum].connected ## GET CONNECTING STATE ##
            # ------------------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Connecting failed', ex)).json

@before(PreProcessRequest(maxdev))
class description:
    def on_get(self, req: Request, resp: Response, devnum: int):
        if devnum == 0 :
            resp.text = PropertyResponse(Switch0Metadata.Description, req).json
        else :
            resp.text = PropertyResponse(Switch1Metadata.Description, req).json

@before(PreProcessRequest(maxdev))
class devicestate:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = []
            # val.append(StateValue('## NAME ##', ## GET VAL ##))
            # Repeat for each of the operational states per the device spec
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'switch.Devicestate failed', ex)).json


class disconnect:
    def on_put(self, req: Request, resp: Response, devnum: int):
        try:
            # ---------------------------
            ### DISCONNECT THE DEVICE ###
            switch_dev[devnum].disconnect()
            # ---------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Disconnect failed', ex)).json

@before(PreProcessRequest(maxdev))
class driverinfo:
    def on_get(self, req: Request, resp: Response, devnum: int):
        if devnum == 0 :
            resp.text = PropertyResponse(Switch0Metadata.Info, req).json
        else :
            resp.text = PropertyResponse(Switch1Metadata.Info, req).json

@before(PreProcessRequest(maxdev))
class interfaceversion:
    def on_get(self, req: Request, resp: Response, devnum: int):
        if devnum == 0 :
            resp.text = PropertyResponse(Switch0Metadata.InterfaceVersion, req).json
        else :
            resp.text = PropertyResponse(Switch1Metadata.InterfaceVersion, req).json

@before(PreProcessRequest(maxdev))
class driverversion():
    def on_get(self, req: Request, resp: Response, devnum: int):
        if devnum == 0 :
            resp.text = PropertyResponse(Switch0Metadata.Version, req).json
        else :
            resp.text = PropertyResponse(Switch1Metadata.Version, req).json

@before(PreProcessRequest(maxdev))
class name():
    def on_get(self, req: Request, resp: Response, devnum: int):
        if devnum == 0 :
            resp.text = PropertyResponse(Switch0Metadata.Name, req).json
        else :
            resp.text = PropertyResponse(Switch1Metadata.Name, req).json

@before(PreProcessRequest(maxdev))
class supportedactions:
    def on_get(self, req: Request, resp: Response, devnum: int):
        if devnum == 0 :
            resp.text = PropertyResponse(['get_tset','get_voltage','get_current'], req).json  # Not PropertyNotImplemented
        else :
            resp.text = PropertyResponse([], req).json  # Not PropertyNotImplemented

@before(PreProcessRequest(maxdev))
class maxswitch:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        try:
            # ----------------------
            val = switch_dev[devnum].maxswitch ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Maxswitch failed', ex)).json

@before(PreProcessRequest(maxdev))
class canwrite:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev[devnum].canwrite(id)
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Canwrite failed', ex)).json

@before(PreProcessRequest(maxdev))
class getswitch:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev[devnum].getswitch(id) ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Getswitch failed', ex)).json

@before(PreProcessRequest(maxdev))
class getswitchdescription:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev[devnum].get_description(id) ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Getswitchdescription failed', ex)).json

@before(PreProcessRequest(maxdev))
class getswitchname:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev[devnum].get_name(id)
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Getswitchname failed', ex)).json

@before(PreProcessRequest(maxdev))
class getswitchvalue:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev[devnum].get_value(id) 
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Getswitchvalue failed', ex)).json

@before(PreProcessRequest(maxdev))
class minswitchvalue:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev[devnum].get_minvalue(id)
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Minswitchvalue failed', ex)).json

@before(PreProcessRequest(maxdev))
class maxswitchvalue:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev[devnum].get_maxvalue(id)
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Maxswitchvalue failed', ex)).json

@before(PreProcessRequest(maxdev))
class switchstep:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev[devnum].get_step(id)
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Switchstep failed', ex)).json

@before(PreProcessRequest(maxdev))
class setswitch:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not  switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        statestr = get_request_field('State', req)      # Raises 400 bad request if missing
        try:
            state = to_bool(statestr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'State {statestr} not a valid boolean.')).json
            return

        try:
            #resp.text = MethodResponse(req, NotImplementedException()).json
            # -----------------------------
            #switch_dev[devnum].set_switch(id)
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Setswitch failed', ex)).json

@before(PreProcessRequest(maxdev))
class setswitchname:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        name = get_request_field('Name', req)         # Raises 400 bad request if missing
        ### INTEPRET AS NEEDED OR FAIL ###  # Raise Alpaca InvalidValueException with details!
        try:
            resp.text = MethodResponse(req,
                            MethodNotImplemented(f'setswitch not implemented.')).json
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Setswitchname failed', ex)).json

@before(PreProcessRequest(maxdev))
class setswitchvalue:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        valuestr = get_request_field('Value', req)      # Raises 400 bad request if missing
        try:
            value = float(valuestr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Value {valuestr} not a valid number.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # -----------------------------
            switch_dev[devnum].set_value(id,value)
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Setswitchvalue failed', ex)).json

@before(PreProcessRequest(maxdev))
class canasync:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = False ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Canasync failed', ex)).json

@before(PreProcessRequest(maxdev))
class statechangecomplete:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = True ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Statechangecomplete failed', ex)).json

@before(PreProcessRequest(maxdev))
class cancelasync:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Cancelasync failed', ex)).json

@before(PreProcessRequest(maxdev))
class setasync:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        statestr = get_request_field('State', req)      # Raises 400 bad request if missing
        try:
            state = to_bool(statestr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'State {statestr} not a valid boolean.')).json
            return

        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Setasync failed', ex)).json

@before(PreProcessRequest(maxdev))
class setasyncvalue:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not switch_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        valuestr = get_request_field('Value', req)      # Raises 400 bad request if missing
        try:
            value = float(valuestr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Value {valuestr} not a valid number.')).json
            return
        if id < 0 or id > switch_dev[devnum].maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Setasyncvalue failed', ex)).json
