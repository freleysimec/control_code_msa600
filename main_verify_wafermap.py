## FRE LEYS OKT 2022 & FEB 2023
import time
import my_setup as mySetup
import my_methods as myMethods
import my_excel_handler as myExcelHandler
import os
import sys


projectLabel = "testje"
projectFolder = r"F:\testje"
mySetup.usedTools = ["PAV", "MSA_600"]


# projectLabel = "playground"
# hardDisk = "D:\\"

### NO TOUCHY TOUCHY ###------------------------------------------------------------

def main():

    ## INITIALISE FILES
    # dataDirectory = os.path.join(hardDisk)
    # projectDirectory = os.path.join(dataDirectory, projectLabel)
    projectDirectory = os.path.join(projectFolder)

    if not os.path.exists(projectDirectory):
        print("Can't find project directory: " + projectDirectory)
        sys.exit()

    ## INITIALISE THE SETUP
    mySetup.initiate()
    mySetup.myPav.move_chuck_separation()

    ## INITIALISE WAFERMAP
    myUserInput = myExcelHandler.UserInput(projectLabel=projectLabel, projectDirectory=projectDirectory)
    myVerifiedWaferMap = myExcelHandler.VerifiedWaferMap(projectLabel=projectLabel, projectDirectory=projectDirectory)

    waferMapDf = myUserInput.waferMapDf
    dieSize = myUserInput.get_die_size()
    dieSizeX = dieSize[0]
    dieSizeY = dieSize[1]

    ## GET COORDINATES OF CENTER Of CHUCK
    mySetup.myPav.move_chuck_relative_to_center(0,0)
    time.sleep(3)
    centerCoordinates = myMethods.get_and_save_coordinates_of_center_of_chuck(myVerifiedWaferMap=myVerifiedWaferMap)
    xCenter = centerCoordinates[0]
    yCenter = centerCoordinates[1]

    ## START MEASUREMENTS
    mySetup.myPav.move_chuck_relative_to_home(0,0)
    time.sleep(1)

    ## FOR ALL DIES:
    for index, die in waferMapDf.iterrows():
        xRelativeToHome = die["DieX"]*dieSizeX
        yRelativeToHome = die["DieY"]*dieSizeY
        xRelativeToCenter = xRelativeToHome + xCenter
        yRelativeToCenter = yRelativeToHome + yCenter

        inRange = xRelativeToCenter > mySetup.myPav.XMIN and xRelativeToCenter < mySetup.myPav.XMAX and yRelativeToCenter > mySetup.myPav.YMIN and yRelativeToCenter < mySetup.myPav.YMAX
        inDiameter = (xRelativeToCenter**2 + yRelativeToCenter**2) < 9025000000

        ## within range
        if inRange and inDiameter:
            mySetup.myPav.move_chuck_relative_to_home( -xRelativeToHome, -yRelativeToHome)
            mySetup.myPav.move_chuck_to_contact()
                    
            # MAPPING
            myMethods.save_coordinates_and_msa600_elevation_semi_auto(dieIndex = index, myVerifiedWaferMap=myVerifiedWaferMap)
            mySetup.myPav.move_chuck_separation()

        ## out of range
        else:
            myMethods.anotate_die_ignored(dieIndex = index, myVerifiedWaferMap=myVerifiedWaferMap)
            print("Die Ignored Because Out of Probe Station Range")


    ## FINISH THE MEASUREMENTS    
    mySetup.myPav.move_chuck_separation()
    mySetup.myPav.move_chuck_relative_to_home(0,0)
    print('DONE: verified wafermap created')


if __name__=='__main__':
    main()
    #exit()