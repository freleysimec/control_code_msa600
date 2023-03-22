from imports import *
import os
import time
import my_setup as mySetup
from post_processing.svd_class import*
import utilities.my_computer_vision as myComputerVision
import my_excel_handler as myExcelHandler
import sys

projectLabel = "20230316_DEFN"
projectFolder = r"D:\Fre\20230316_DEFN"
# averaging = 1
# points = 1
averaging = 20
points = 10
sampleTime = 0.256   #s




### NO TOUCHY TOUCHY ###------------------------------------------------------------

def main():

    ## INITIALISE SETUP & TOOLS
    mySetup.initiate()
    time.sleep(1)
    mySetup.myPav.move_chuck_separation()
    
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
    myPerformedMeasurements = myExcelHandler.MeasurementOutput(projectLabel = projectLabel, projectDirectory=projectDirectory)
    myVerifiedWaferMap = myExcelHandler.VerifiedWaferMap(projectLabel=projectLabel, projectDirectory=projectDirectory)

    
    ## INITIATE MEASUREMENT
    
    ## FOR ALL MEASUREMENTS
    myMeasurements = myUserInput.get_measurements()
    for measurementIndex, measurement in myMeasurements.iterrows():
        if not measurementIndex == "abreviation":    

            # MOVE CHUCK TO POI IF DIE NOT IGNORED
            dieIndex = measurement["die index"]
            dieCoordinates = myVerifiedWaferMap.get_coordinates_of_die(dieIndex)
            theta = myVerifiedWaferMap.get_theta(dieIndex)
            mySetup.myPav.move_theta(theta = theta)
            mySetup.myPav.move_chuck_relative_to_home( -dieCoordinates[0], -dieCoordinates[1])

            # GET PARAMETERS
            measurementName = myUserInput.get_experiment_filename(measurementIndex)
            svdFileName = measurementName + ".svd"
            svdFile = os.path.join(resultsDirectory, svdFileName)
            settingsFileName = myUserInput.get_settings_file(measurementIndex=measurementIndex)
            settingsFile = os.path.join(settingsDirectory, settingsFileName)



            ## PERFORM MEASUREMENT 

            # SELECT THE MSA-600 SETTINGS
            mySetup.myMsa600.change_settings(settingsPath = settingsFile)


            # # SELECT THE SETTINGS FOR THE VOLTAGE ACTUATION
            # mySetup.myAwgExt.set_sweep_settings(startFrequency=1000, stopFrequency=25000000, sweepTime=0.028, voltage= 1)
            mySetup.myAwgExt.output_off()
            
            # START SCAN AND SAVE RESULTS
            mySetup.myMsa600.send_scan_request_and_trigger_awg(resultspath = svdFile, myAwgExt= mySetup.myAwgExt, timeLimitForResponse= 20, averaging = averaging, points = points ,sampleTime = sampleTime)
            
            ## SAVE PERFORMED MEASUREMENT
            measurementData = {
                #"RF": resonananceFrequency,
            }
            
            myPerformedMeasurements.save_measurement_datas(measurementIndex, measurementData, name=measurementName)
        

            
        # break
    
    ## FINISH THE MEASUREMENTS    
    mySetup.myPav.move_chuck_separation()
    mySetup.myPav.move_chuck_relative_to_home(0,0)
    thetaHome = myVerifiedWaferMap.get_theta(dieIndex = "r2c3")
    mySetup.myPav.move_theta(theta=thetaHome)

    print('Measurements finished')


if __name__ == "__main__":
    main()


#TODO: computer vision: autofocus
#TODO: computer vision: align: set constants
#TODO: get all data from msa-settings info file
#TODO: improve averaging: from settings file
#TODO: implement multiple scan points: scan points in excell file
#TODO: email polytec with error en question set settings

#TODO: remaining time estimate
#TODO: tutorial code sharing (first check Conda)
#TODO: get awg inputs from userInput
#TODO: more natural Wafermap input (1-23 in excel)
#TODO: mySetup as class
#TODO: simplify code: one rule for "FOR ALL MEASUREMENTS" for loop
#TODO: Fré Quality factor for RF
#TODO: select measurements based on measurement index
