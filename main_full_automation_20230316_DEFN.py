import os
import time
from msa_aquisition_settings_class import MsaAquisitionSettings
from  my_setup_class import MySetup
from post_processing.svd_class import*
import utilities.my_computer_vision as myComputerVision
import my_excel_handler as myExcelHandler
import sys

projectLabel = "20230316_DEFN"
projectFolder = r"D:\Fre\20230316_DEFN"
usedTools = ["PAV", "AWG_EXT", "MSA_600"]


# averaging = 1
# points = 1
# averaging = 20
# points = 10
# sampleTime = 0.256   #s




### NO TOUCHY TOUCHY ###------------------------------------------------------------

def main():

    ## INITIALISE SETUP & TOOLS
    mySetup = MySetup(usedTools = usedTools)
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

            
            # GET MSA-600 SETTINGS
            settingsFileName = myUserInput.get_settings_file(measurementIndex=measurementIndex)
            settingsFile = os.path.join(settingsDirectory, settingsFileName)
            myMsaAquisitionSettings = MsaAquisitionSettings(settingsDirectory, settingsFile)    

            # GET PARAMETERS
            measurementName = myUserInput.get_experiment_filename(measurementIndex)
            svdFileName = measurementName + ".svd"
            svdFile = os.path.join(resultsDirectory, svdFileName)
            settingsFileName = myUserInput.get_settings_file(measurementIndex=measurementIndex)
            settingsFile = os.path.join(settingsDirectory, settingsFileName)

            # MOVE CHUCK TO POI
            dieIndex = measurement["die index"]
            dieCoordinates = myVerifiedWaferMap.get_coordinates_of_die(dieIndex)
            theta = myVerifiedWaferMap.get_theta(dieIndex)
            mySetup.myPav.move_theta(theta = theta)
            mySetup.myPav.move_chuck_relative_to_home( -dieCoordinates[0], -dieCoordinates[1])



            ## PERFORM MEASUREMENT 

            # SELECT THE MSA-600 SETTINGS
            mySetup.myMsa600.change_settings(settingsFile = settingsFile)
            mySetup.myAwgExt.output_off()
            
            # START SCAN AND SAVE RESULTS
            mySetup.myMsa600.send_scan_request_and_trigger_awg(resultspath = svdFile, myAwgExt= mySetup.myAwgExt, timeLimitForResponse= 20, myMsaAquisitionSettings =myMsaAquisitionSettings)
            
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
