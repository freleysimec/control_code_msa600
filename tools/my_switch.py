# -*- coding: utf-8 -*-
"""
Created OCT 2022
@author: Fré Leys
"""

import time

class SWIclass(object):

    switches = {'smu' : ['1106', '1204'],
                'scs' : ['1112', '1214'],
                'awg' : ['1108', '1210'], #former fgen
                'lcr' : ['1101', '1202']}

    def __init__(self, RM, port):
        self.RM = RM
        self.port = port

    def id(self):
        self.handler = self.RM.open_resource(self.SWIport)
        #self.handler.clear()
        self.handler.read_termination = '\n'
        self.handler.write_termination = '\n'
        self.handler.timeout = 30000

        self.respo = self.handler.query('*IDN?')
        self.handler.close()
        return self.respo
    
    def open_all_switches(self):
        
        self.handler = self.RM.open_resource(self.port)
        self.handler.clear()
        #print(self.handler)
        #time.sleep(1)
        self.handler.read_termination = '\n'
        self.handler.write_termination = '\n'
        self.handler.timeout = 30000
        self.handler.write('channel.open("allslots")')
        time.sleep(0.3)
        self.handler.close()
        return 'All switches open.'
    
    def close_smu(self,):
        self.SMUswitches = self.switches['smu']
        self.handler = self.RM.open_resource(self.SWIport)
        self.handler.clear()
        self.handler.read_termination = '\n'
        self.handler.write_termination = '\n'
        self.handler.timeout = 30000

        for i in self.SMUswitches:
            #print('SWI smu', i)
            self.handler.write('channel.close("' + i + '")')

        time.sleep(0.3)
        self.handler.close()
        
    def close_scs(self,):
        self.SCSswitches = self.switches['scs']
        #print('SCS switches: ', self.SCSswitches)
        self.handler = self.RM.open_resource(self.port)
        self.handler.clear()
        self.handler.read_termination = '\n'
        self.handler.write_termination = '\n'
        self.handler.timeout = 30000

        for i in self.SCSswitches:
            #print('SWI scs', i)
            self.handler.write('channel.close("' + i + '")')

        time.sleep(0.3)
        self.handler.close()

    def close_lcr(self,):
        self.LCRswitches = self.switches['lcr']
        self.handler = self.RM.open_resource(self.port)
        self.handler.clear()
        self.handler.read_termination = '\n'
        self.handler.write_termination = '\n'
        self.handler.timeout = 30000

        for i in self.LCRswitches:
            #print('SWI lcr', i)
            self.handler.write('channel.close("' + i + '")')

        time.sleep(0.3)
        self.handler.close()

    def close_ext_awg(self,):
        self.AWGswitches = self.switches['awg']

        self.handler = self.RM.open_resource(self.port)
        self.handler.clear()
        self.handler.read_termination = '\n'
        self.handler.write_termination = '\n'
        self.handler.timeout = 30000

        for i in self.AWGswitches:
            #print('SWI awg', i)
            self.handler.write('channel.close("' + i + '")')

        time.sleep(0.3)
        self.handler.close()

    def closeNi6363(self,):
        self.AWGswitches = self.switches['awg']
        self.handler = self.RM.open_resource(self.port)
        self.handler.clear()
        self.handler.read_termination = '\n'
        self.handler.write_termination = '\n'
        self.handler.timeout = 30000

        for i in self.AWGswitches:
            #print('SWI awg', i)
            self.handler.write('channel.close("' + i + '")')

        time.sleep(0.3)
        self.handler.close()
