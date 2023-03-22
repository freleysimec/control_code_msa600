from imports import *
import os
import time
import my_setup as mySetup
from post_processing.svd_class import*
import utilities.my_computer_vision as myComputerVision
import my_excel_handler as myExcelHandler
import sys

projectLabel = "cv_test"
projectFolder = r"D:\Fre\cv_test"
#settingsFileFrequency = "reference_image.set"
averaging = 1



### NO TOUCHY TOUCHY ###------------------------------------------------------------

def main():

    ## INITIALISE SETUP & TOOLS
    mySetup.initiate()
    time.sleep(1)
    mySetup.myPav.move_chuck_align()
    mySetup.myPav.move_probe_relative_to_home(0,0)

    ## INITIALISE FILES
    # controlCodeDirectory = os.getcwd()
    projectDirectory = os.path.join(projectFolder)
    resultsDirectory = os.path.join(projectDirectory, "results")
    settingsDirectory = os.path.join(projectDirectory, "msa600 settings")
    imagesDirectory = os.path.join(resultsDirectory, "images")

    if not os.path.exists(projectDirectory):
        print("Can't find project directory: " + projectDirectory)
        sys.exit()
    if not os.path.exists(resultsDirectory):
        os.makedirs(resultsDirectory)    
    if not os.path.exists(imagesDirectory):
        os.makedirs(imagesDirectory)

    myUserInput = myExcelHandler.UserInput(projectLabel=projectLabel, projectDirectory=projectDirectory)
    myVerifiedWaferMap = myExcelHandler.VerifiedWaferMap(projectLabel=projectLabel, projectDirectory=projectDirectory)
    myPerformedMeasurements = myExcelHandler.MeasurementOutput(projectLabel = projectLabel, projectDirectory=projectDirectory)

    ## INITIATE MEASUREMENT
    try:
        centerCoordinates = myVerifiedWaferMap.get_coordinates_of_center_of_chuck()
    except:
        print("no center coordinates given so setting the; to home coordinates")
        centerCoordinates =[0,0]
    mySetup.myPav.set_center_coordinates(centerCoordinates = centerCoordinates)
    
    ## FOR ALL MEASUREMENTS
    myMeasurements = myUserInput.get_measurements()
    for measurementIndex, measurement in myMeasurements.iterrows():
        if not measurementIndex == "abreviation":    
            initialTime = time.time()

            # MOVE CHUCK TO POI IF DIE NOT IGNORED
            dieIndex = measurement["die index"]
            dieCoordinates = myVerifiedWaferMap.get_coordinates_of_die(dieIndex)
            
            if (not dieCoordinates[0] == "IGNORED"):
                
                #get structure coordinates
                try:
                    structureIndex = measurement["structure index"]                    
                    structureCoordinatesRelativeToDie = myUserInput.get_structure_coordinates_relative_to_die_home(structureIndex)
                except:
                    print("no structure index found: measuring at die home coordinates")
                    structureCoordinatesRelativeToDie = [0,0]
                
                xStructureRelativeToCenter = dieCoordinates[0] + mySetup.myPav.xCenter + structureCoordinatesRelativeToDie[0]
                yStructureRelativeToCenter = dieCoordinates[1] + mySetup.myPav.yCenter + structureCoordinatesRelativeToDie[0]
                xStructureRelativeToHome = dieCoordinates[0] + structureCoordinatesRelativeToDie[0]
                yStructureRelativeToHome = dieCoordinates[1] + structureCoordinatesRelativeToDie[1]

                #if structure in range
                inRange = xStructureRelativeToCenter > mySetup.myPav.XMIN and xStructureRelativeToCenter < mySetup.myPav.XMAX and yStructureRelativeToCenter > mySetup.myPav.YMIN and yStructureRelativeToCenter < mySetup.myPav.YMAX
                inDiameter = (xStructureRelativeToCenter**2 + yStructureRelativeToCenter**2) < 9025000000
                if inRange and inDiameter:
                    
                    # GET SETTINGS FILE
                    settingsFile = myUserInput.get_settings_file(measurementIndex=measurementIndex)
                    settingsPath = os.path.join(settingsDirectory, settingsFile)

                    experimentName = myUserInput.get_experiment_filename(measurementIndex)
                    fileNameSVD = experimentName + "_resonanceFrequency.svd"
                
                    # Move chuck to sum of die AND structure coordinates (opgelet, verified wafer is chuck coordinates en structure coordinates tegengestelde assen)
                    mySetup.myPav.move_chuck_relative_to_home( -xStructureRelativeToHome, -yStructureRelativeToHome)

                    # Move MSA-600 to focus height
                    verifiedElevation = myVerifiedWaferMap.get_verified_msa600_elevation_at_die(dieIndex)
                    mySetup.myPav.move_probe_z(verifiedElevation) 
                    initialMsa600Coordinates = mySetup.myPav.get_probe_coordinates_relative_to_home()
                    print(initialMsa600Coordinates)




                    # MOVE SCOPE TO EXACT POSITION
                    print("move scope")
                    imageName = "image_measurement_{}".format(measurementIndex)

                    myComputerVision.take_and_save_image(imagesDirectory=imagesDirectory, imageName = imageName, mySetup=mySetup)
                    time.sleep(3)
                    scopeTranslation = myComputerVision.get_translation_between_myImage_and_reference_image(imagesDirectory=imagesDirectory, myImage = imageName + ".png", referenceImageName = "referenceImage.png")
                    print("scopeTranslation")

                    newXcoord = float(initialMsa600Coordinates[1]) - scopeTranslation[0]
                    print(newXcoord)
                    newYcoord = float(initialMsa600Coordinates[2]) - scopeTranslation[1]
                    print(newYcoord)

                    mySetup.myPav.move_probe_relative_to_home(x = newXcoord, y = newYcoord)






                    # PERFORM MEASUREMENT 
                    print("x postion: " + str(dieCoordinates[0]))
                    print("y postion: " + str(dieCoordinates[1]))
                    mySetup.myPav.move_chuck_to_contact()

                    # SELECT THE MSA-600 SETTINGS
                    mySetup.myMsa600.change_settings(settingsPath = settingsPath)

                    # SELECT THE SETTINGS FOR THE VOLTAGE ACTUATION
                    mySetup.myAwgExt.set_sweep_settings(startFrequency=1000, stopFrequency=25000000, sweepTime=0.028, voltage= 1)

                    # START SCAN AND SAVE RESULTS
                    resultspath = os.path.join(resultsDirectory, fileNameSVD)
                    mySetup.myMsa600.send_scan_request_and_trigger_awg(resultspath, myAwgExt= mySetup.myAwgExt, timeLimitForResponse= 20, averaging = averaging, triggerOpenTime=1)

                    # # DETERMINE THE RESONANCE FREQUENCY FROM THE MEASUREMENT DATA
                    # mySVD = Svd(resultsDirectory = resultsDirectory,  filename = fileNameSVD)
                    # resonananceFrequency = mySVD.get_resonance_frequency(point=1,fMin=1000000, fMax=24000000)
                    # print("resonananceFrequency: " + str(resonananceFrequency))
                    
                    ## SAVE performed measurement in "measurements done file" (links measurement number with MSA600 file number)
                    resonananceFrequency= 19
                    measurementData = {
                        "RF": resonananceFrequency,
                    }
                    
                    myPerformedMeasurements.save_measurement_datas(measurementIndex, measurementData, name=experimentName)

                else:
                    print("measurement Ignored because Structure not in Range")
                    ## SAVE performed measurement in "measurements done file" (anotate IGNORED under DIE)
                    myPerformedMeasurements.save_measurement_as_ignored(measurementIndex, "IGNORED STRUCTURE")

            else:
                print("measurement Ignored because Die not in Range")
                ## SAVE performed measurement in "measurements done file" (anotate IGNORED under DIE)
                myPerformedMeasurements.save_measurement_as_ignored(measurementIndex, "IGNORED")
                
            # break

    ## FINISH THE MEASUREMENTS    
    mySetup.myPav.move_chuck_separation()
    mySetup.myPav.move_chuck_relative_to_home(0,0)
    print('Measurements finished')

if __name__ == "__main__":
    main()


#TODO: get all data from msa-settings info file
#TODO: email polytec with error en question set settings
#TODO: remaining time estimate
#TODO: get awg inputs from userInput
#TODO: mySetup as class
#TODO: select measurements based on measurement index
#TODO: simplify code: one rule for "FOR ALL MEASUREMENTS" for loop
#TODO: more natural Wafermap input (1-23 in excel)




#TODO: computer vision: add rotation
#TODO: computer vision: align: set constants
#TODO: computer vision: autofocus

#TODO: implement multiple scan points: scan point indexes in excell file
#TODO: tutorial code sharing (first check Conda)
#TODO: Fré Quality factor for RF
