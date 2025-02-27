# routines for use with Shelyak eShel spectograph and calibration channel

import socket
import sys, getopt
import time
from time import sleep
try: from serial import Serial
except: print('no serial')

#    Copyright (c) 2007, 2015 by jerch (brejoe@web.de)
#
#    This program is free software; you can redistribute it and#or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the
#    Free Software Foundation, Inc.,
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# -*- coding: utf-8 -*-


class K8056(object):
    """
    K8056 - Class for controlling the velleman K8056 8 channel relay card
    K8056(device, repeat=0, wait=0)
    Give serial port as number or device file.
    For better reliability repeat instructions `repeat` times
    and `wait` seconds between execution.
    """
    def __init__(self, port='COM4', repeat=0, wait=1, logger=None):
        self._serial = Serial(port, 2400)
        self.repeat = repeat
        self.wait = wait
        self.maxswitch = 4
        self.minswitchvalue = 0
        self.maxswitchvalue = 1
        self.description = ['quartz','ThAr','LED','Mirror']
        self.canasync = False
        self.connect()
        sleep(0.1)

    def connect(self) :
        print('connecting K8056...')
        self.clear(9)
        self.state = 0
        self.connected = True

    def disconnect(self):
        '''Close underlying serial device connection.'''
        self._serial.close()
        
    def _process(self, instruction, byte, address):
        cksum = (243 - instruction - byte - address) & 255
        for i in range(self.repeat + 1):
            self._serial.write(bytearray([13, address, instruction, byte, cksum]))
            sleep(self.wait)
        
    def set(self, relay, address=1):
        '''Set `relay` (9 for all) of card at `address` (default 1).'''
        if not 0 < relay < 10:
            raise Exception('invalid relay number')
        self._process(83, relay+48, address&255)
        
    def clear(self, relay, address=1):
        '''Clear `relay` (9 for all) of card at `address` (default 1).'''
        if not 0 < relay < 10:
            raise Exception('invalid relay number')
        self._process(67, relay+48, address&255)
        
    def toggle(self, relay, address=1):
        '''Toggle `relay` (9 for all) of card at `address` (default 1).'''
        if not 0 < relay < 10:
            raise Exception('invalid relay number')
        self._process(84, relay+48, address&255)
        
    def set_address(self, new=1, address=1):
        '''Set address of card at `address` to `new`.'''
        self._process(65, new&255, address&255)
       
    def set_state(self,id,state) :
        if state :
            val = self.state | 1 << id+4
        else :
            val = self.state & ~(1 << id+4)

        print('sending: ', val)
        self.send_byte(val)
        self.state = val

    def getswitch(self,id) :
        val = self.state & (1 << id+4)
        if val > 0 : return True
        else : return False
 
    def send_byte(self, num, address=1):
        '''Set relays to `num` (in binary mode).'''
        self._process(66, num&255, address&255)

    def emergency_stop(self):
        '''Clear all relays on all cards. emergency purpose.'''
        self._process(69, 1, 1)
        
    def force_address(self):
        '''Reset all cards to address 1.'''
        self._process(70, 1, 1)
        
    def get_address(self):
        '''Display card address on LEDs.'''
        self._process(68, 1, 1)

    def canwrite(self,id) :
        return True

    def get_description(self,id) :
        return self.description[id]

    def get_value(self,id) : 
        return self.getstate(self,id)

    def get_minvalue(self,id) :
        return self.minswitchvalue

    def get_maxvalue(self,id) :
        return self.maxswitchvalue

    def get_step(self,id) :
        return 1
