"""
Created OCT 2022
@author: Fré Leys, originally Piotr Czarnecki
"""


#import imp
import time

class PAVclass(object):

    XMIN = -76350
    XMAX = 76680
    YMIN = -76520
    YMAX = 74970
    xCenter = 0
    yCenter = 0
    
    def __init__(self, RM, port):
        self.RM = RM
        self.port = port
        self.XMIN = -76350
        self.XMAX = 76680
        self.YMIN = -76520
        self.YMAX = 74970

    def id(self):
        self.handler = self.RM.open_resource(self.port)
        self.handler.read_termination = '\r\n'
        self.handler.write_termination = '\r\n'
        self.handler.timeout = 30000

        self.handler.clear()
        self.handler.query('ReadSystemStatus')
        self.respo = self.handler.query('ReadSystemStatus')
        
        self.handler.close()
        return self.respo

    def set_center_coordinates(self, centerCoordinates):
         self.xCenter = centerCoordinates[0]
         self.yCenter = centerCoordinates[1]

    def move_chuck_separation(self):
        self.handler = self.RM.open_resource(self.port)
        self.handler.read_termination = '\r\n'
        self.handler.write_termination = '\r\n'
        self.handler.timeout = 30000
        self.handler.clear()
        self.handler.query('ReadSystemStatus')

        self.respo = self.handler.query('MoveChuckSeparation')
        self.handler.close()
        return self.respo
    
    def move_chuck_align(self):
        self.handler = self.RM.open_resource(self.port)
        self.handler.read_termination = '\r\n'
        self.handler.write_termination = '\r\n'
        self.handler.timeout = 30000
        self.handler.clear()
        self.handler.query('ReadSystemStatus')

        self.respo = self.handler.query('MoveChuckAlign')
        self.handler.close()
        return self.respo

    def move_chuck_to_contact(self):
        self.handler = self.RM.open_resource(self.port)
        self.handler.read_termination = '\r\n'
        self.handler.write_termination = '\r\n'
        self.handler.timeout = 30000
        
        self.handler.clear()
        self.handler.query('ReadSystemStatus')
        
        self.respo = self.handler.query('MoveChuckContact')
        self.handler.close()
        return self.respo

    def move_chuck_relative_to_home(self, x, y):
            self.x = x
            self.y = y
            self.origin = "H"
            self.move_chuck(x, y, self.origin)

    def move_chuck_relative_to_center(self, x, y):
            self.x = x
            self.y = y
            self.origin = "C"
            self.move_chuck(x, y, self.origin)

    def move_chuck(self, x, y, origin):
        self.x = x
        self.y = y
        self.origin = origin
        self.handler = self.RM.open_resource(self.port)
        self.handler.read_termination = '\r\n'
        self.handler.write_termination = '\r\n'
        self.handler.timeout = 30000

        self.handler.clear()
        self.handler.query('ReadSystemStatus')

        self.respo = self.handler.query('MoveChuck ' + str(self.x) + ' ' + str(self.y) + ' ' + self.origin)   #PAV Remote Interface P82/91: 
        self.handler.close()
        return self.respo

    def move_probe_z(self, z):
        self.handler = self.RM.open_resource(self.port)
        self.handler.read_termination = '\r\n'
        self.handler.write_termination = '\r\n'
        self.handler.timeout = 30000

        self.handler.clear()
        self.handler.query('ReadSystemStatus')

        self.respo = self.handler.query('MoveProbeZ ' + str(4) + ' ' + str(z)) 
        self.handler.close()
        return self.respo
     
    def move_scope(self, x, y, origin):
        self.x = x
        self.y = y
        self.origin = origin

        self.handler = self.RM.open_resource(self.port)
        self.handler.read_termination = '\r\n'
        self.handler.write_termination = '\r\n'
        self.handler.timeout = 30000

        self.handler.clear()
        self.handler.query('ReadSystemStatus')

        self.respo = self.handler.query('MoveScope ' + str(self.x) + ' ' + str(self.y) + ' ' + self.origin)
        self.handler.close()
        return self.respo

    def move_scope_relative_to_home(self, x, y):
        self.x = x
        self.y = y
        self.origin = "H"
        self.move_scope(x, y, self.origin)
        print('moved scope to x: ' + str(self.x) + ' y: ' + str(self.y) + ' relative to home')

        time.sleep(1)

    def get_chuck_coordinates(self):
        self.handler = self.RM.open_resource(self.port)
        self.handler.read_termination = '\r\n'
        self.handler.write_termination = '\r\n'
        self.handler.timeout = 30000

        self.handler.clear()
        self.handler.query('ReadSystemStatus')

        self.respo = self.handler.query('ReadChuckPosition')    #default: in micron & relative to home [p87]
        self.handler.close()
        chuckCoordinates = self.respo.split(':')[1].split()
        return chuckCoordinates
    
    def get_probe_coordinates(self):
        self.handler = self.RM.open_resource(self.port)
        self.handler.read_termination = '\r\n'
        self.handler.write_termination = '\r\n'
        self.handler.timeout = 30000

        self.handler.clear()
        self.handler.query('ReadSystemStatus')

        self.respo = self.handler.query('ReadProbePosition ' + str(4))    # the MSA-600 is attached to a stage that is controlled by probe 4
        self.handler.close()
        probeCoordinates = self.respo.split(':')[1].split()

        return probeCoordinates
