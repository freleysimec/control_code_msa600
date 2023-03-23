import pyvisa               #$ pip install -U pyvisa // pip3 install pyvisa-py // pip install pyserial
from tools.my_switch import *
from tools.my_awg import *
from tools.my_pav import *
from tools.my_msa600 import *

RM = pyvisa.ResourceManager()
tools = {
            'SWITCH' : {'port': 'USB0::0x05E6::0x3706::04368023::INSTR', 'termination': '\n', 'id_message': '*IDN?'},
            'AWG_EXT' : {'port': 'USB0::0x0957::0x4807::MY53302026::INSTR', 'termination': '\n', 'id_message': '*IDN?'},
            'PAV' : {'port': 'ASRL6::INSTR', 'termination': '\r\n', 'id_message': 'ReadSystemStatus'},
            'MSA_600' : {'port': 'ASRL8::INSTR', 'termination': '\r', 'id_message': '*IDN?'},
              }

# if "CAMERA" in usedTools :
#     from tools.my_screen_capturer import *
#     myCamera = ScreenCapturer()

# CONNECTIONS FOR TOOLS CONTROLLED BY PYVISA
# USB[board]::manufacturer ID::model code::serial number[::USB interface number][::INSTR]


class MySetup(object):
    def __init__(self, usedTools):
        self.tools = tools
        self.RM = RM
        self.usedTools = usedTools

    def initiate(self):
        print('checking the status of all devices:')
        if "SWITCH" in self.usedTools :
            swiPort = tools['SWITCH']['port']
            self.mySwi = SWIclass()
            print('SWITCH: ', swiPort, self.mySwi.id())
        else : 
            print('SWITCH: NOT ENABLED in my_inputs.py')

        if "AWG_EXT" in self.usedTools   :
            awgPort = tools['AWG_EXT']['port']
            self.myAwgExt = AWGclass(RM=RM, port=awgPort)   
            print('AWG EXT: ', awgPort, self.myAwgExt.id())
        else : 
            print('AWG EXT: NOT ENABLED in my_inputs.py')

        if "MSA_600" in self.usedTools  :
            self.myMsa600= MSA600() 
            print("MSA_600: Don't forget to run the macro")
        else : 
            print('MSA_600: NOT ENABLED in my_inputs.py')

        if "PAV" in self.usedTools   :
            pavPort = tools['PAV']['port']
            self.myPav = PAVclass(RM = RM, port=pavPort)
            print('PAV: ', pavPort, self.myPav.id())
        else : 
            print('PAV: NOT ENABLED in my_inputs.py')


