## FRE LEYS OKT 2022 & FEB 2023

import time
import my_setup as mySetup
import my_methods as myMethods
import my_excel_handler as myExcelHandler
import numpy as np

filename = "my_testje"
filenameVerifiedWafer = filename +"_verified_wafer"

def main():

    ## INITIALISE THE SETUP
    mySetup.initiate()
    mySetup.myPav.move_chuck_separation()

    ## INITIALISE WAFERMAP
    myUserInput = myExcelHandler.UserInput(filename)
    waferMap = myUserInput.get_wafer_map()
    dieSize = myUserInput.get_die_size()

    ## GET COORDINATES OF CENTER Of CHUCK
    mySetup.myPav.move_chuck_relative_to_center(0,0)
    time.sleep(3)
    centerCoordinates = myMethods.get_and_save_coordinates_of_center_of_chuck(filename=filenameVerifiedWafer)
    xCenter = centerCoordinates[0]
    yCenter = centerCoordinates[1]

    pavXMin = -76350
    pavXMax = 76680
    pavYMin = -76520
    pavYMax = 74970

    ## START MEASUREMENTS
    mySetup.myPav.move_chuck_relative_to_home(0,0)
    #mySetup.myPav.move_scope_relative_to_home(0,0)
    time.sleep(1)

    ## FOR ALL DIES:
    for i, die in enumerate(waferMap):
        #TODO: if die is within range:
        xRelativeToHome = die[0]*dieSize[0]
        yRelativeToHome = die[1]*dieSize[1]
        xRelativeToCenter = xRelativeToHome + xCenter
        yRelativeToCenter = yRelativeToHome + yCenter

        inRange = xRelativeToCenter > pavXMin and xRelativeToCenter < pavXMax and yRelativeToCenter > pavYMin and yRelativeToCenter < pavYMax
        inDiameter = (xRelativeToCenter**2 + yRelativeToCenter**2) < 9025000000

        ## within range
        if inRange and inDiameter:
            mySetup.myPav.move_chuck_relative_to_home( -xRelativeToHome, -yRelativeToHome)
            mySetup.myPav.move_chuck_align()
            print("Press T if coordinates are OK")
                    
            # MAPPING
            myMethods.save_coordinates_of_die_home_point(dieIndex = i, filename=filenameVerifiedWafer)
            mySetup.myPav.move_chuck_separation()

        ## out of range ttt
        else:
            myMethods.anotate_die_ignored(dieIndex = i, filename=filenameVerifiedWafer)
            print("Die Ignored Because Out of Probe Station Range")


    ## FINISH THE MEASUREMENTS    
    mySetup.myPav.move_chuck_separation()
    mySetup.myPav.move_chuck_relative_to_home(0,0)
    print('DONE: verified wafermap created')


if __name__=='__main__':
    main()
    #exit()