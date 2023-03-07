import time
import os
from tools.my_awg import *


class MSA600(object):
    def __init__(self):
        self.communicationDirectory = "msa600_macros"
        self.requestFileName = "requests.txt"
        self.responseFileName = "response.txt"

    # CREATE REQUESTS & WAIT FOR RESPONSE & IF FOUND READ RESPONSE & DELETE RESPONSE FILE
    def send_requests(self, requests, timeLimitForResponse = 10):
        response = ""

        # CREATE COMMUNICATION DIRECTORY IF IT DOES NOT EXIST
        if not os.path.exists(self.communicationDirectory):
            os.makedirs(self.communicationDirectory)
        
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

    def send_scan_request_and_trigger_awg(self,request, myAwgExt:  AWGclass, timeLimitForResponse = 10, triggerWaitTime = 2, triggerOpenTime = 1, averaging =1):
        response = ""

        # CREATE COMMUNICATION DIRECTORY IF IT DOES NOT EXIST
        if not os.path.exists(self.communicationDirectory):
            os.makedirs(self.communicationDirectory)
        
        # CREATE REQUESTS 
        with open(os.path.join(self.communicationDirectory, self.requestFileName), 'w') as f:
            for line in request:
                f.write(line + "\n")
        print("Request sent")
        
        # TRIGGER AWG AFTER 1.5 S (AcquisitionSlave.bas loops every second)
        time.sleep(triggerWaitTime)
        for i in range(averaging):
            myAwgExt.awg_trigger(triggerOpenTime=triggerOpenTime)
        
        
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