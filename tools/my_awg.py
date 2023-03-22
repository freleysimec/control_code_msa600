# -*- coding: utf-8 -*-
"""
Created OCT 2022
@author: Fré Leys
"""

import time        


class AWGclass(object):
    def __init__(self, RM, port):
        self.RM = RM
        self.port = port

    def id(self):
        self.handler = self.RM.open_resource(self.port)
        self.handler.clear()
        self.handler.read_termination = '\n'
        self.handler.write_termination = '\n'
        self.handler.timeout = 30000
        #self.handler.write('*RST')
        self.respo = self.handler.query('*IDN?')
        self.handler.close()
        return self.respo

    def set_sweep_settings(self, voltage, startFrequency, stopFrequency, sweepTime):
        
        instr = self.RM.open_resource(self.port)
        instr.write('OUTP1:LOAD 50')    #'OUTP1:LOAD INF'
        instr.write('OUTP1:SYNC:SOUR CH1')
        instr.write('TRIG1:SOUR BUS')

        instr.write('SOUR1:FUNC SIN')
        instr.write('SOUR1:VOLT ' + str(voltage))
        instr.write('SOUR1:FREQ:MODE SWE')
        instr.write('SWE:STAT ON')
        instr.write('SOUR1:FREQ:STAR '+str(startFrequency))     #100
        instr.write('SOUR1:FREQ:STOP '+str(stopFrequency))      #4e3
        instr.write('SOUR1:SWE:TIME ' + str(sweepTime))         #3.2
        
        instr.close()
        
    def set_sine_settings(self, peakToPeakAmplitude, frequency, offset = 0):
        
        instr = self.RM.open_resource(self.port)
        
        instr.write('OUTP1:LOAD 50')    #'OUTP1:LOAD INF'
        instr.write('OUTP1:SYNC:SOUR CH1')
        instr.write('TRIG1:SOUR BUS')
        instr.write('SWE:STAT OFF')
        
        instr.write('SOUR1:FUNC SIN')
        instr.write('SOUR1:VOLT '+ str(peakToPeakAmplitude))
        instr.write('SOUR1:FREQ:MODE FIX')
        instr.write('SOUR1:FREQ ' + str(frequency))
        time.sleep(1)

        instr.close()

    def output_off(self):
        instr = self.RM.open_resource(self.port)
        time.sleep(0.5)
        instr.write('OUTP1 OFF')
        instr.write('OUTP:SYNC OFF')
        time.sleep(0.5)
        instr.close()
        
    def awg_trigger(self, triggerOpenTime):
        
        # instr = self.RM.open_resource(self.port)

        # instr.write('OUTPUT1 ON')
        # time.sleep(0.5)
        # instr.write('OUTP:SYNC ON')
        # time.sleep(0.5)
        # instr.write('TRIG')
        # print('START TRIGGER') 
        # time.sleep(triggerOpenTime)
        # instr.write('OUTP1 OFF')
        # instr.write('OUTP:SYNC OFF')
        # print('END TRIGGER') 
        # time.sleep(0.5)
        # instr.close()
        instr = self.RM.open_resource(self.port)

        instr.write('OUTPUT1 ON')
        time.sleep(0.5)
        instr.write('OUTP:SYNC ON')
        time.sleep(triggerOpenTime)
        instr.write('OUTP1 OFF')
        instr.write('OUTP:SYNC OFF')
        print('END TRIGGER') 
        time.sleep(0.5)
        instr.close()
              
    def reset_config(self):

        instr = self.RM.open_resource(self.port)

        instr.write('*RST')
        time.sleep(1)
        instr.write('OUTP1:50')    #'OUTP1:LOAD INF'
        time.sleep(0.5)

        instr.write('OUTP:SYNC:SOUR CH1')
        instr.write('OUTP1 OFF')
        instr.write('OUTP1:SYNC OFF')
        time.sleep(0.5)
        
        instr.close()

    def setupVoltageActuationSignalDV(self, peakToPeakAmplitude, frequency, amountOfCycles):
        
        self.actuation_voltage_amplitude = peakToPeakAmplitude
        self.actuation_frequency = frequency
        self.actuation_burst_pulses = amountOfCycles
        self.handler = self.RM.open_resource(self.port)
        #self.handler.clear()
        self.handler.read_termination = '\n'
        self.handler.write_termination = '\n'
        self.handler.timeout = 30000
                                                                                    # see p421 for an example
        self.handler.write('SWE:STAT OFF')                                          # Disable sweep
        self.handler.write('SOUR1:FUNC RAMP')                                       # The FUNCtion subsystem configures the instrument's output function:
        self.handler.write('SOUR1:FUNC:RAMP:SYMM 50')                               # Sets the symmetry percentage for ramp waves. [p290]
        self.handler.write('SOUR1:VOLT ' + str(self.actuation_voltage_amplitude))
        self.handler.write('SOUR1:VOLT:OFFS:+0.0')
        self.handler.write('SOUR1:FREQ ' + str(self.actuation_frequency))

        time.sleep(1)

        self.handler.write('BURS:MODE TRIG')
        self.handler.write('TRIG1:SOUR EXT')
        self.handler.write('BURS:INT:PER 1')                                        # p228 set burst period: the interval at which bursts are generated => 1s // here ignored because external trigger
        self.handler.write('BURS:NCYC ' + str(self.actuation_burst_pulses))         # p229 set amount of cycles: the number of cycles in a burst
        self.handler.write('BURS:STAT ON')
        self.handler.write('OUTP ON')
        
        #self.handler.write('TRIG')                                                  # Trigger the burst/ why here? 
        time.sleep(1)

        self.handler.close()
        time.sleep(1)

        return ('AWG for DV sweep is ready.')



