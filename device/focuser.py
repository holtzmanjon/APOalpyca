
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# focuser.py - Alpaca API responders for Focuser
#
# Author:   Jon Holtzman < holtz@nmsu.edu >
#
# -----------------------------------------------------------------------------
# Edit History:
#   Generated by Python Interface Generator for AlpycaDevice
#
# 02-Jan-2025   Initial edit

from falcon import Request, Response, HTTPBadRequest, before
from logging import Logger
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \
                StateValue, get_request_field, to_bool
from exceptions import *        # Nothing but exception classes

logger: Logger = None

# ----------------------
# MULTI-INSTANCE SUPPORT
# ----------------------
# If this is > 0 then it means that multiple devices of this type are supported.
# Each responder on_get() and on_put() is called with a devnum parameter to indicate
# which instance of the device (0-based) is being called by the client. Leave this
# set to 0 for the simple case of controlling only one instance of this device type.
#
maxdev = 2                      # Single instance

# -----------
# DEVICE INFO
# -----------
# Static metadata not subject to configuration changes
class FocuserMetadata:
    """ Metadata describing the Focuser Device. Edit for your device"""
    Name = 'Zaber Focuser'
    Version = 'V1.0.0'
    Description = 'Zaber Focuser'
    DeviceType = 'Focuser'
    DeviceID = 'ca2c7a00-6664-40b6-aa49-2e90d8e2ce06'
    Info = 'Alpaca Sample Device\nImplements IFocuser\nASCOM Initiative'
    MaxDeviceNumber = maxdev
    InterfaceVersion = 3        # IFocuserVxxx

class StageMetadata:
    """ Metadata describing the Switch Device. Edit for your device"""
    Name = 'Thorlabs LTS Stage'
    Version = '1.0.0'
    Description = 'LTS Stage'
    DeviceType = 'Focuser'
    DeviceID = '75a88d87-15da-4d2f-94ba-612cd5bb0fea'
    DeviceID2 = 'b93157f1-c8dc-4f9d-8214-ff6c5fdb21ac'
    Info = 'Alpaca Sample Device\nImplements ISwitch\nASCOM Initiative'
    MaxDeviceNumber = 2
    InterfaceVersion = 3

from zaber_stage import Zaber
from lts150 import LTS150

focuser_dev = None
def start_focuser_device(logger: logger):
    logger = logger
    global focuser_dev
    focuser_dev = [Zaber(logger=logger),
                   LTS150(logger=logger,serial_no="45441684",name='Iodine stage'),
                   LTS150(logger=logger,serial_no="45494294",name='Calibration stage')]

# --------------------
# RESOURCE CONTROLLERS
# --------------------

@before(PreProcessRequest(maxdev))
class action:
    def on_put(self, req: Request, resp: Response, devnum: int):
        if req.get_media()['Action'] == 'home' :
            focuser_dev[devnum].home()
            #resp.text = MethodResponse(req).json
            resp.text = PropertyResponse('home',req).json

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
            focuser_dev[devnum].init()
            # ------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Focuser.Connect failed', ex)).json

@before(PreProcessRequest(maxdev))
class connected:
    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # -------------------------------------
            is_conn = focuser_dev[devnum].connected
            # -------------------------------------
            resp.text = PropertyResponse(is_conn, req).json
        except Exception as ex:
            resp.text = MethodResponse(req, DriverException(0x500, 'Focuser.Connected failed', ex)).json

@before(PreProcessRequest(maxdev))
class connecting:
    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # ------------------------------
            val = focuser_dev[devnum].connected
            # ------------------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Focuser.Connecting failed', ex)).json

@before(PreProcessRequest(maxdev))
class description:
    def on_get(self, req: Request, resp: Response, devnum: int):
        if devnum == 0 :
            resp.text = PropertyResponse(FocuserMetadata.Description, req).json
        else :
            resp.text = PropertyResponse(StageMetadata.Description, req).json

@before(PreProcessRequest(maxdev))
class devicestate:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
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
                            DriverException(0x500, 'focuser.Devicestate failed', ex)).json


class disconnect:
    def on_put(self, req: Request, resp: Response, devnum: int):
        try:
            # ---------------------------
            focuser_dev[devnum].disconnect()
            # ---------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Focuser.Disconnect failed', ex)).json

@before(PreProcessRequest(maxdev))
class driverinfo:
    def on_get(self, req: Request, resp: Response, devnum: int):
        if devnum == 0 :
            resp.text = PropertyResponse(FocuserMetadata.Info, req).json
        else :
            resp.text = PropertyResponse(StageMetadata.Info, req).json

@before(PreProcessRequest(maxdev))
class interfaceversion:
    def on_get(self, req: Request, resp: Response, devnum: int):
        if devnum == 0 :
            resp.text = PropertyResponse(FocuserMetadata.InterfaceVersion, req).json
        else :
            resp.text = PropertyResponse(StageMetadata.InterfaceVersion, req).json

@before(PreProcessRequest(maxdev))
class driverversion():
    def on_get(self, req: Request, resp: Response, devnum: int):
        if devnum == 0 :
            resp.text = PropertyResponse(FocuserMetadata.Version, req).json
        else :
            resp.text = PropertyResponse(StageMetadata.Version, req).json

@before(PreProcessRequest(maxdev))
class name():
    def on_get(self, req: Request, resp: Response, devnum: int):
        if devnum == 0 :
            resp.text = PropertyResponse(FocuserMetadata.Name, req).json
        elif devnum == 1 :
            resp.text = PropertyResponse('Iodine stage', req).json
        elif devnum == 2 :
            resp.text = PropertyResponse('Calibration stage', req).json

@before(PreProcessRequest(maxdev))
class supportedactions:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(['home'], req).json

@before(PreProcessRequest(maxdev))
class absolute:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        try:
            # ----------------------
            val = focuser_dev[devnum].get_position()
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Focuser.Absolute failed', ex)).json

@before(PreProcessRequest(maxdev))
class ismoving:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        

        try:
            # ----------------------
            val = focuser_dev[devnum].is_moving()
            # ----------------------
            resp.text = PropertyResponse(val, req).json
            return
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Focuser.Ismoving failed', ex)).json

@before(PreProcessRequest(maxdev))
class maxincrement:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        try:
            # ----------------------
            #val = ## GET PROPERTY ##
            # ----------------------
            #resp.text = PropertyResponse(val, req).json
            resp.text = MethodResponse(req, NotImplementedException()).json
            return
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Focuser.Maxincrement failed', ex)).json

@before(PreProcessRequest(maxdev))
class maxstep:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        try:
            # ----------------------
            #val = ## GET PROPERTY ##
            # ----------------------
            #resp.text = PropertyResponse(val, req).json
            resp.text = MethodResponse(req, NotImplementedException()).json
            return
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Focuser.Maxstep failed', ex)).json

@before(PreProcessRequest(maxdev))
class position:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        try:
            # ----------------------
            val = focuser_dev[devnum].get_position()
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Focuser.Position failed', ex)).json

@before(PreProcessRequest(maxdev))
class stepsize:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        try:
            # ----------------------
            #val = ## GET PROPERTY ##
            # ----------------------
            #resp.text = PropertyResponse(val, req).json
            resp.text = MethodResponse(req, NotImplementedException()).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Focuser.Stepsize failed', ex)).json

@before(PreProcessRequest(maxdev))
class tempcomp:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        try:
            # ----------------------
            #val = ## GET PROPERTY ##
            # ----------------------
            #resp.text = PropertyResponse(val, req).json
            resp.text = MethodResponse(req, NotImplementedException()).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Focuser.Tempcomp failed', ex)).json

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        tempcompstr = get_request_field('TempComp', req)      # Raises 400 bad request if missing
        try:
            tempcomp = to_bool(tempcompstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'TempComp {tempcompstr} not a valid boolean.')).json
            return

        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Focuser.Tempcomp failed', ex)).json

@before(PreProcessRequest(maxdev))
class tempcompavailable:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        try:
            # ----------------------
            val = False
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Focuser.Tempcompavailable failed', ex)).json

@before(PreProcessRequest(maxdev))
class temperature:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        try:
            # ----------------------
            #val = ## GET PROPERTY ##
            # ----------------------
            #resp.text = PropertyResponse(val, req).json
            resp.text = MethodResponse(req, NotImplementedException()).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Focuser.Temperature failed', ex)).json

@before(PreProcessRequest(maxdev))
class halt:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            #resp.text = MethodResponse(req).json
            resp.text = MethodResponse(req, NotImplementedException()).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Focuser.Halt failed', ex)).json

@before(PreProcessRequest(maxdev))
class move:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not focuser_dev[devnum].connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        positionstr = get_request_field('Position', req)      # Raises 400 bad request if missing
        try:
            position = int(positionstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Position {positionstr} not a valid integer.')).json
            return
        if position < focuser_dev[devnum].get_minvalue() or position > focuser_dev[devnum].get_maxvalue() :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Value " + position + " not in range.')).json
            return

        try:
            # -----------------------------
            focuser_dev[devnum].set_position(position)
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Focuser.Move failed', ex)).json

