import time
import csv
import user_input_pumba as userInput
import utilities.my_timer as myTimer
import utilities.my_logger as myLogger
# import my_setup as mySetup
# import utilities.my_logger as myLogger


def main():
     ## INITIALISE THE LOG FILE
     myTimer.setT0()
     myLogger.createNewLogFile()

     # ## INITIALISE THE SETUP
     # mySetup.checkStatus()

     ## MANUALLY MOVE CHUCK TO FIRST POI
     
     ## FOR ALL DIES:
     with open(userInput.waferMapLocation, 'r') as csvfile:
          waferMap = csv.reader(csvfile, delimiter=',', quotechar='|')
          for i, die in enumerate(waferMap):
               if i > 0: # The first row of the "WaferMap" CSV file has to be skipped.  
                    
                    # MOVE CHUCK TO POI
                    # mySetup.myPav.MoveChuckRelativeToHome( int(die[0]), int(die[1])) #using adjusted wafermap
                    # myLogger.logNewLineWithTimeStamp("Moved chuck to die [" + str(die[0]) + "," + str(die[1]) + "]") 
                    # dieID = "DIE_" + str(die[0]) + str(die[1])

                    # PERFORM MEASUREMENT 
                    print(die[0])
                    print(die[1])

                    # mySetup.myPav.MoveChuckContact()
                    # time.sleep(2)


if __name__=='__main__':
     main()
