import time
import os
from tools.my_awg import *


class MSA600(object):
    def __init__(self):
        self.communicationDirectory = "msa600_macros"
        self.requestFileName = "requests.txt"
        self.responseFileName = "response.txt"
        
        # CREATE COMMUNICATION DIRECTORY IF IT DOES NOT EXIST
        if not os.path.exists(self.communicationDirectory):
            os.makedirs(self.communicationDirectory)

    # CREATE REQUESTS & WAIT FOR RESPONSE & IF FOUND READ RESPONSE & DELETE RESPONSE FILE
    def send_requests(self, requests, timeLimitForResponse = 10):
        response = ""

        # CREATE REQUESTS 
        with open(os.path.join(self.communicationDirectory, self.requestFileName), 'w') as f:
            for line in requests:
                f.write(line + "\n")
        print("Request sent")
        
        # WAIT FOR RESPONSE & IF FOUND READ RESPONSE & DELETE RESPONSE FILE
        start_time = time.time()
        while (time.time() - start_time) < timeLimitForResponse:
            if os.path.exists(os.path.join(self.communicationDirectory, self.responseFileName)):
                with open(os.path.join(self.communicationDirectory, self.responseFileName), 'r') as f:
                    response = f.read()
                    print("Response received: " + response)
                os.remove(os.path.join(self.communicationDirectory, self.responseFileName))
                break
            time.sleep(1)

        if (time.time() - start_time) >= timeLimitForResponse:
            print("Timeout: No response of the MSA600 received within " + str(timeLimitForResponse) + " seconds." + "Did you forget to run the macro?")
        
        return response

    def send_scan_request_and_trigger_awg(self,resultspath, myAwgExt:  AWGclass, myMsaAquisitionSettings,  timeLimitForResponse = 10, triggerWaitTime = 2):
        response = ""
        requests = ["SCAN_AND_SAVE," + str(resultspath)]

        # CREATE REQUESTS 
        with open(os.path.join(self.communicationDirectory, self.requestFileName), 'w') as f:
            for line in requests:
                f.write(line + "\n")
        print("Request sent")
        
        ## Repeat for all points: 
        time.sleep(triggerWaitTime)
        for i in range(myMsaAquisitionSettings.measurementPointsCount):
            print("point: "+str(i+1))
            ## TRIGGER AWG AFTER 1.5 S (AcquisitionSlave.bas loops every second)
            # trigger the amount of averaging and wait for at least 
            for i in range(myMsaAquisitionSettings.averageCount):
                myAwgExt.awg_trigger(triggerOpenTime=myMsaAquisitionSettings.sampleTime)
                # time.sleep(sampleTime)
        # for i in range(points):
        #     print("point: "+str(i+1))
        #     ## TRIGGER AWG AFTER 1.5 S (AcquisitionSlave.bas loops every second)
        #     myAwgExt.awg_trigger(triggerOpenTime=0.01)
        
        # WAIT FOR RESPONSE & IF FOUND READ RESPONSE & DELETE RESPONSE FILE
        start_time = time.time()
        while (time.time() - start_time) < timeLimitForResponse:
            if os.path.exists(os.path.join(self.communicationDirectory, self.responseFileName)):
                with open(os.path.join(self.communicationDirectory, self.responseFileName), 'r') as f:
                    response = f.read()
                    print("Response received: " + response)
                os.remove(os.path.join(self.communicationDirectory, self.responseFileName))
                break
            time.sleep(1)

        if (time.time() - start_time) >= timeLimitForResponse:
            print("Timeout: No response of the MSA600 received within " + str(timeLimitForResponse) + " seconds." + "Did you forget to run the macro?")
        
        return response
    
    def change_settings(self, settingsFile):
        requests = ["CHANGE_SETTINGS," + str(settingsFile)]
        self.send_requests(requests, timeLimitForResponse= 20)
