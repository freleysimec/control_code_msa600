import os
import time
from msa_aquisition_settings_class import MsaAquisitionSettings
from my_setup_class import MySetup
from post_processing.svd_class import*
import my_excel_handler as myExcelHandler
import sys

projectLabel = "testje"
projectFolder = r"F:\testje"




settingsFileFrequency = "pumba_frequency.set"
settingsFileAmplitude = "pumba_amplitude.set"
# averaging = 10

### NO TOUCHY TOUCHY ###------------------------------------------------------------

def main():

    ## INITIALISE FILES
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


    ## INITIALISE SETUP & 
    usedTools = myUserInput.get_used_tools()
    mySetup = MySetup(usedTools = usedTools)
    mySetup.initiate()
    time.sleep(1)
    mySetup.myPav.move_chuck_align()

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
            
            if not dieCoordinates[0] == "IGNORED":
                
                #get structure coordinates
                try:
                    structureIndex = measurement["structure index"]                    
                    structureCoordinatesRelativeToDie = myUserInput.get_structure_coordinates_relative_to_die_home(structureIndex)
                except:
                    print("no structure index found")
                    structureCoordinatesRelativeToDie = [0,0]
                
                xStructureRelativeToCenter = dieCoordinates[0] + mySetup.myPav.xCenter + structureCoordinatesRelativeToDie[0]
                yStructureRelativeToCenter = dieCoordinates[1] + mySetup.myPav.yCenter + structureCoordinatesRelativeToDie[0]
                xStructureRelativeToHome = dieCoordinates[0] + structureCoordinatesRelativeToDie[0]
                yStructureRelativeToHome = dieCoordinates[1] + structureCoordinatesRelativeToDie[1]



                ## FOR ALL MEASUREMENTS IN RANGE
                inRange = xStructureRelativeToCenter > mySetup.myPav.XMIN and xStructureRelativeToCenter < mySetup.myPav.XMAX and yStructureRelativeToCenter > mySetup.myPav.YMIN and yStructureRelativeToCenter < mySetup.myPav.YMAX
                inDiameter = (xStructureRelativeToCenter**2 + yStructureRelativeToCenter**2) < 9025000000
                if inRange and inDiameter:
                    
                    # GET PAV SETTINGS
                    verifiedElevation = myVerifiedWaferMap.get_verified_msa600_elevation_at_die(dieIndex)
                    #theta = myVerifiedWaferMap.get_theta(dieIndex)

                    # GET MSA-600 SETTINGS
                    # settingsFileName = myUserInput.get_settings_file(measurementIndex=measurementIndex)
                    # settingsFile = os.path.join(settingsDirectory, settingsFileName)
                    settingsFileFrequency = os.path.join(settingsDirectory, settingsFileFrequency)
                    myMsaAquisitionSettingsFrequency = MsaAquisitionSettings(settingsDirectory, settingsFileFrequency)
                    settingsFileAmplitude = os.path.join(settingsDirectory, settingsFileAmplitude)
                    myMsaAquisitionSettingsAmplitude = MsaAquisitionSettings(settingsDirectory, settingsFileAmplitude)
                    
                    # GET AWG_EXT SETTINGS
                    awgExtSettings = myUserInput.get_awg_ext_settings(measurementIndex=measurementIndex)

                    # GET SVD NAMES
                    measurementName = myUserInput.get_experiment_filename(measurementIndex)
                    fileNameResonanceFrequencySVD = measurementName + "_resonanceFrequency.svd"
                    fileNameResonanceAmplitudeSVD = measurementName + "_amplitude.svd"
                
                    # MOVE CHUCK TO POI
                    # mySetup.myPav.move_theta(theta = theta)
                    mySetup.myPav.move_chuck_relative_to_home( -xStructureRelativeToHome, -yStructureRelativeToHome)
                    mySetup.myPav.move_probe_z(verifiedElevation) 

                    # PERFORM MEASUREMENT 
                    print("x postion: " + str(dieCoordinates[0]))
                    print("y postion: " + str(dieCoordinates[1]))
                    mySetup.myPav.move_chuck_to_contact()

                    # SELECT THE MSA-600 SETTINGS
                    mySetup.myMsa600.change_settings(settingsFile = settingsFileFrequency)
                    mySetup.myAwgExt.change_settings (settings = awgExtSettings[0])

                    # START FREQUENCY SCAN AND SAVE RESULTS
                    mySetup.myMsa600.send_scan_request_and_trigger_awg(resultspath = fileNameResonanceFrequencySVD, myAwgExt= mySetup.myAwgExt, timeLimitForResponse= 20, myMsaAquisitionSettings =myMsaAquisitionSettingsFrequency)

                    # DETERMINE THE RESONANCE FREQUENCY FROM THE MEASUREMENT DATA
                    mySVD = Svd(resultsDirectory = resultsDirectory,  filename = fileNameResonanceFrequencySVD)
                    resonananceFrequency = mySVD.get_resonance_frequency(point=1,fMin=1000000, fMax=24000000)
                    print("resonananceFrequency: " + str(resonananceFrequency))
                    


                    ### AMPLITUDE SCAN

                    # SELECT THE MSA-600 SETTINGS
                    mySetup.myMsa600.change_settings(settingsFile = settingsFileAmplitude)
                    mySetup.myAwgExt.change_settings (settings = awgExtSettings[1])
                    
                    # START SCAN AND SAVE RESULTS
                    mySetup.myMsa600.send_scan_request_and_trigger_awg(resultspath = fileNameResonanceFrequencySVD, myAwgExt= mySetup.myAwgExt, timeLimitForResponse= 20, myMsaAquisitionSettings =myMsaAquisitionSettingsAmplitude)

                    # DETERMINE THE DISPLACEMENT AMPLITUDE FROM THE MEASUREMENT DATA
                    mySVD = Svd(resultsDirectory = resultsDirectory,  filename = fileNameResonanceAmplitudeSVD)
                    displacementAmplitude = mySVD.get_displacement_amplitude(point=1)

                    # DETERMINE THE ACTUATION AMPLITUDE FROM THE MEASUREMENT DATA
                    actuationAmplitude = mySVD.get_actuation_amplitude(point=1)
                    relativeDisplacementAmplitude = displacementAmplitude/actuationAmplitude
                    
                    ## SAVE performed measurement in "measurements done file" (links measurement number with MSA600 file number)
                    # save images as link
                    measurementData = {
                        "RF": resonananceFrequency,
                        "V": actuationAmplitude,
                        "D/V": relativeDisplacementAmplitude,
                    }
                    
                    myPerformedMeasurements.save_measurement_datas(measurementIndex, measurementData, name=measurementName)

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
