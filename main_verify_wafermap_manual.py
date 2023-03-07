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


### NO TOUCHY TOUCHY ###------------------------------------------------------------

def main():

    ## INITIALISE FILES
    projectDirectory = os.path.join(projectFolder)

    if not os.path.exists(projectDirectory):
        print("Can't find project directory: " + projectDirectory)
        sys.exit()

    ## INITIALISE THE SETUP
    mySetup.initiate()
    mySetup.myPav.move_chuck_separation()

    ## INITIALISE WAFERMAP
    myVerifiedWaferMap = myExcelHandler.VerifiedWaferMap(projectLabel=projectLabel, projectDirectory=projectDirectory)

    ## CAPTURE COORDINATES & FOCUS HEIGHT
    finished = False
    while finished == False:
        dieName = input("Enter the name (index) for your the die you are taking the coordinates of and press enter: ")
        finished = myMethods.save_coordinates_and_msa600_elevation_manual(dieIndex = dieName, myVerifiedWaferMap=myVerifiedWaferMap)
        mySetup.myPav.move_chuck_separation()

    ## FINISH THE MEASUREMENTS    
    mySetup.myPav.move_chuck_separation()
    mySetup.myPav.move_chuck_relative_to_home(0,0)
    print('DONE: verified wafermap created')


if __name__=='__main__':
    main()
    #exit()