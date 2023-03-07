import pyvisa               #$ pip install -U pyvisa // pip3 install pyvisa-py // pip install pyserial


RM = pyvisa.ResourceManager()

tools = {
            'SWITCH' : {'port': 'USB0::0x05E6::0x3706::04368023::INSTR', 'termination': '\n', 'id_message': '*IDN?'},
            'AWG_EXT' : {'port': 'USB0::0x0957::0x4807::MY53302026::INSTR', 'termination': '\n', 'id_message': '*IDN?'},
            'PAV' : {'port': 'ASRL7::INSTR', 'termination': '\r\n', 'id_message': 'ReadSystemStatus'},
            'MSA_600' : {'port': 'ASRL8::INSTR', 'termination': '\r', 'id_message': '*IDN?'},
              }


class MSA600class(object):
    def __init__(self, RM, port):
        self.RM = RM
        self.port = port
        pass

    def id(self):
        self.RM = self.RM
        self.MSVport = self.port
        self.handler = self.RM.open_resource(self.port)
        self.handler.clear()
        self.handler.read_termination = '\r'
        self.handler.write_termination = '\r'
        self.handler.timeout = 30000
        self.respo = self.handler.query('*IDN?')
        self.handler.close()
        return self.respo
    
msa600Port = tools['MSA_600']['port']
myMsa600= MSA600class(RM, msa600Port) 
print("jos")

print('MSA_600: ', msa600Port, myMsa600.id())



