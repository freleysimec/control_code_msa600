## FRE LEYS OKT 2022 & FEB 2023
import time
from my_setup_class import MySetup
import my_methods as myMethods
import my_excel_handler as myExcelHandler
import os
import sys
import utilities.my_computer_vision as myComputerVision


projectLabel = "20230316_DEFN"
projectFolder = r"D:\Fre\20230316_DEFN"
usedTools = ["PAV", "MSA_600"]


### NO TOUCHY TOUCHY ###------------------------------------------------------------

def main():

    ## INITIALISE FILES
    projectDirectory = os.path.join(projectFolder)
    resultsDirectory = os.path.join(projectDirectory, "results")
    imagesDirectory = os.path.join(resultsDirectory, "images")

    if not os.path.exists(projectDirectory):
        print("Can't find project directory: " + projectDirectory)
        sys.exit()
    if not os.path.exists(resultsDirectory):
        os.makedirs(resultsDirectory)    
    if not os.path.exists(imagesDirectory):
        os.makedirs(imagesDirectory)

    ## INITIALISE THE SETUP
    mySetup = MySetup(usedTools = usedTools)
    mySetup.initiate()
    mySetup.myPav.move_chuck_separation()

    ## INITIALISE WAFERMAP
    myVerifiedWaferMap = myExcelHandler.VerifiedWaferMap(projectLabel=projectLabel, projectDirectory=projectDirectory)

    # ## TAKE AND SAVE REFERENCE IMAGE
    # myReferenceInputImageIsOk = input("move MSA600 (not the chuck!!) to the reference location and press enter when ready:")
    # myComputerVision.take_and_save_reference_image(imagesDirectory=imagesDirectory, mySetup=mySetup)

    ## CAPTURE COORDINATES, THETA & FOCUS HEIGHT
    finished = False
    while finished == False:
        finished = myMethods.save_chuck_position_and_msa600_elevation_manual( myVerifiedWaferMap=myVerifiedWaferMap)
        mySetup.myPav.move_chuck_separation()

    ## FINISH THE MEASUREMENTS    
    mySetup.myPav.move_chuck_separation()
    mySetup.myPav.move_chuck_relative_to_home(0,0)
    thetaHome = myVerifiedWaferMap.get_theta(dieIndex = "r2c3")
    print("thetaHome: " + str(thetaHome))
    mySetup.myPav.move_theta(theta=thetaHome)
    
    print('DONE: verified wafermap created')


if __name__=='__main__':
    main()
    #exit()