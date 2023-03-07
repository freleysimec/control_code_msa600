import pyvisa               #$ pip install -U pyvisa // pip3 install pyvisa-py // pip install pyserial
import my_excel_handler as myExcelHandler

#myUserInput = myExcelHandler.UserInput("canopus")
#usedTools = myUserInput.get_tools()
usedTools = ["PAV", "AWG_EXT", "MSA_600"]

RM = pyvisa.ResourceManager()

tools = {
            'SWITCH' : {'port': 'USB0::0x05E6::0x3706::04368023::INSTR', 'termination': '\n', 'id_message': '*IDN?'},
            'AWG_EXT' : {'port': 'USB0::0x0957::0x4807::MY53302026::INSTR', 'termination': '\n', 'id_message': '*IDN?'},
            'PAV' : {'port': 'ASRL6::INSTR', 'termination': '\r\n', 'id_message': 'ReadSystemStatus'},
            'MSA_600' : {'port': 'ASRL8::INSTR', 'termination': '\r', 'id_message': '*IDN?'},
              }



if "SWITCH" in usedTools :
    from tools.my_switch import *
    swiPort = tools['SWITCH']['port']
    mySwi = SWIclass()

if "CAMERA" in usedTools :
    from tools.my_screen_capturer import *
    myCamera = ScreenCapturer()

if "AWG_EXT" in usedTools  :
    from tools.my_awg import *
    awgPort = tools['AWG_EXT']['port']
    myAwgExt = AWGclass(RM=RM, port=awgPort)   

if "MSA_600" in usedTools  :
    from tools.my_msa600 import *
    myMsa600= MSA600() 

if "PAV" in usedTools :
    from tools.my_pav import *
    pavPort = tools['PAV']['port']
    myPav = PAVclass(RM = RM, port=pavPort)


# CONNECTIONS FOR TOOLS CONTROLLED BY PYVISA
# USB[board]::manufacturer ID::model code::serial number[::USB interface number][::INSTR]

# INITIALIZE TOOLS

def initiate():
    print('checking the status of all devices:')
    if "SWITCH" in usedTools:
        print('SWITCH: ', swiPort, mySwi.id())
    else : 
        print('SWITCH: NOT ENABLED in my_inputs.py')

    if "AWG_EXT" in usedTools  :
        print('AWG EXT: ', awgPort, myAwgExt.id())
    else : 
        print('AWG EXT: NOT ENABLED in my_inputs.py')

    if "MSA_600" in usedTools :
        print("MSA_600: Don't forget to run the macro")
    else : 
        print('MSA_600: NOT ENABLED in my_inputs.py')

    if "PAV" in usedTools  :
        print('PAV: ', pavPort, myPav.id())
    else : 
        print('PAV: NOT ENABLED in my_inputs.py')


