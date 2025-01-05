
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# safetymonitor.py - Alpaca API responders for Safetymonitor
#
# Author:   Jon Holtzman < holtz@nmsu.edu > 
#
# -----------------------------------------------------------------------------
# Edit History:
#   Generated by Python Interface Generator for AlpycaDevice
#
# 2024   Initial edit

from falcon import Request, Response, HTTPBadRequest, before
from logging import Logger
from APOSafety import Safety
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \
                get_request_field, to_bool
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
maxdev = 0                      # Single instance

# -----------
# DEVICE INFO
# -----------
# Static metadata not subject to configuration changes
class SafetymonitorMetadata:
    """ Metadata describing the Safetymonitor Device. Edit for your device"""
    Name = 'APO Safety Monitor'
    Version = '0.0.1 '
    Description = 'APO Safetymonitor'
    DeviceType = 'Safetymonitor'
    DeviceID = '3eb59fbc-f718-42d2-9404-90beae9f588e' # https://guidgenerator.com/online-guid-generator.aspx
    Info = 'Alpaca Sample Device\nImplements ISafetymonitor\nASCOM Initiative'
    MaxDeviceNumber = maxdev
    InterfaceVersion = 2        # ISafetymonitorVxxx

# --------------------
# SAFETY ()
# --------------------
safety_dev = None
# At app init not import :-)
def start_safety_device(logger: logger):
    logger = logger
    global safety_dev
    safety_dev = Safety(logger=logger)

# --------------------
# RESOURCE CONTROLLERS
# --------------------
import pdb
@before(PreProcessRequest(maxdev))
class action:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json
        if not safety_dev.connected : ##IS DEV CONNECTED##:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            if req.get_media()['Action'] == 'stat35m' :
                val,val2 = safety_dev.stat() 
                resp.text = PropertyResponse(val, req).json
            elif req.get_media()['Action'] == 'stat25m' :
                val = safety_dev.encl25Open() 
                resp.text = PropertyResponse(val, req).json
            elif req.get_media()['Action'] == 'override' :
                t = req.get_media()['Parameters']
                safety_dev.setoverride(float(t)) 
                resp.text = PropertyResponse(True, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                DriverException(0x500, 'Safetymonitor.Action failed', ex)).json

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
class connected:
    def on_get(self, req: Request, resp: Response, devnum: int):
        # -------------------------------
        is_conn = safety_dev.connected  ### READ CONN STATE ###
        # -------------------------------
        resp.text = PropertyResponse(is_conn, req).json

    def on_put(self, req: Request, resp: Response, devnum: int):
        conn_str = get_request_field('Connected', req)
        conn = to_bool(conn_str)              # Raises 400 Bad Request if str to bool fails
        try:
            # --------------------------------
            ### CONNECT/DISCONNECT()PARAM) ###
            # --------------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req, DriverException(0x500, 'Safetymonitor.Connected failed', ex)).json

@before(PreProcessRequest(maxdev))
class description:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SafetymonitorMetadata.Description, req).json

@before(PreProcessRequest(maxdev))
class driverinfo:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SafetymonitorMetadata.Info, req).json

@before(PreProcessRequest(maxdev))
class interfaceversion:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SafetymonitorMetadata.InterfaceVersion, req).json

@before(PreProcessRequest(maxdev))
class driverversion():
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SafetymonitorMetadata.Version, req).json

@before(PreProcessRequest(maxdev))
class name():
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SafetymonitorMetadata.Name, req).json

@before(PreProcessRequest(maxdev))
class supportedactions:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(['stat35m','stat25m','override'], req).json  # Not PropertyNotImplemented

@before(PreProcessRequest(maxdev))
class issafe:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not safety_dev.connected : ##IS DEV CONNECTED##:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = safety_dev.issafe() ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Safetymonitor.Issafe failed', ex)).json

