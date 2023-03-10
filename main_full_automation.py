from imports import *
import os
import time
import my_setup as mySetup
from post_processing.svd_class import*
import my_excel_handler as myExcelHandler
import sys

projectLabel = "testje"
projectFolder = r"F:\testje"

settingsFileFrequency = "pumba_frequency.set"
settingsFileAmplitude = "pumba_amplitude.set"
averaging = 10



### NO TOUCHY TOUCHY ###------------------------------------------------------------

def main():

    ## INITIALISE SETUP & TOOLS
    mySetup.initiate()
    time.sleep(1)
    mySetup.myPav.move_chuck_align()

    ## INITIALISE FILES
    # controlCodeDirectory = os.getcwd()
    projectDirectory = os.path.join(projectFolder)
    resultsDirectory = os.path.join(projectDirectory, "results")
    settingsDirectory = os.path.join(projectDirectory, "msa600 settings")

    if not os.path.exists(projectDirectory):
        print("Can't find project directory: " + projectDirectory)
        sys.exit()
    if not os.path.exists(resultsDirectory):
        os.makedirs(resultsDirectory)

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

            # GET SETTINGS FILE
            settingsFile = myUserInput.get_settings_file(measurementIndex=measurementIndex)

            # MOVE CHUCK TO POI IF DIE NOT IGNORED
            dieIndex = measurement["die index"]
            dieCoordinates = myVerifiedWaferMap.get_coordinates_of_die(dieIndex)
            verifiedElevation = myVerifiedWaferMap.get_verified_msa600_elevation_at_die(dieIndex)
            
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

                    experimentName = myUserInput.get_experiment_filename(measurementIndex)
                    fileNameSVD = experimentName + "_resonanceFrequency.svd"
                
                    # Move chuck to sum of die AND structure coordinates (opgelet, verified wafer is chuck coordinates en structure coordinates tegengestelde assen)
                    mySetup.myPav.move_chuck_relative_to_home( -xStructureRelativeToHome, -yStructureRelativeToHome)

                    # Move MSA-600 to focus height
                    mySetup.myPav.move_probe_z(verifiedElevation) 

                    # MOVE SCOPE TO EXACT POSITION
                    # mymethods...

                    # PERFORM MEASUREMENT 
                    print("x postion: " + str(dieCoordinates[0]))
                    print("y postion: " + str(dieCoordinates[1]))
                    mySetup.myPav.move_chuck_to_contact()

                    # SELECT THE MSA-600 SETTINGS
                    settingsPath = os.path.join(settingsDirectory, settingsFile)
                    requests = ["CHANGE_SETTINGS," + str(settingsPath)]
                    mySetup.myMsa600.send_requests(requests, timeLimitForResponse= 20)

                    # SELECT THE SETTINGS FOR THE VOLTAGE ACTUATION
                    mySetup.myAwgExt.set_sweep_settings(startFrequency=1000, stopFrequency=25000000, sweepTime=0.028, voltage= 1)

                    # START SCAN AND SAVE RESULTS
                    resultspath = os.path.join(resultsDirectory, fileNameSVD)
                    requests = ["SCAN_AND_SAVE," + str(resultspath)]
                    mySetup.myMsa600.send_scan_request_and_trigger_awg(requests, myAwgExt= mySetup.myAwgExt, timeLimitForResponse= 20, averaging = averaging, triggerOpenTime=1)

                    # DETERMINE THE RESONANCE FREQUENCY FROM THE MEASUREMENT DATA
                    mySVD = Svd(resultsDirectory = resultsDirectory,  filename = fileNameSVD)
                    resonananceFrequency = mySVD.get_resonance_frequency(point=1,fMin=1000000, fMax=24000000)
                    print("resonananceFrequency: " + str(resonananceFrequency))
                    
                    ## SAVE performed measurement in "measurements done file" (links measurement number with MSA600 file number)
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


#TODO: get settingsfile from userInput
#TODO: computer vision: autofocus
#TODO: get all data from msa-settings info file
#TODO: improve averaging: from settings file
#TODO: implement multiple scan points: scan points in excell file

#TODO: email polytec with error en question set settings
#TODO: remaining time estimate
#TODO: tutorial code sharing
#TODO: get awg inputs from userInput
#TODO: more natural Wafermap input (1-23 in excel)
#TODO: mySetup as class
#TODO: simplify code: one rule for "FOR ALL MEASUREMENTS" for loop
#TODO: rename excel file tabs
#TODO: Fré Quality factor for RF
#TODO: select measurements based on measurement index
