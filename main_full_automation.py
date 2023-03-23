import os
import time
from my_setup_class import MySetup
from msa_aquisition_settings_class import MsaAquisitionSettings
from post_processing.svd_class import*
import utilities.my_computer_vision as myComputerVision
import my_excel_handler as myExcelHandler
import sys

projectLabel = "pumba1_oval"
projectFolder = r"C:\Users\leys40\OneDrive - imec\_MEASUREMENTS\PUMBA\pumba1_oval"

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


    ## INITIALISE SETUP & TOOLS
    usedTools = myUserInput.get_used_tools()
    mySetup = MySetup(usedTools = usedTools)
    mySetup.initiate()
    time.sleep(1)
    if usedTools.__contains__("PAV"):  mySetup.myPav.move_chuck_align()
    if usedTools.__contains__("PAV"):  mySetup.myPav.move_probe_relative_to_home(0,0)




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



                ## FOR ALL MEASUREMENTS IN RANGE
                inRange = xStructureRelativeToCenter > mySetup.myPav.XMIN and xStructureRelativeToCenter < mySetup.myPav.XMAX and yStructureRelativeToCenter > mySetup.myPav.YMIN and yStructureRelativeToCenter < mySetup.myPav.YMAX
                inDiameter = (xStructureRelativeToCenter**2 + yStructureRelativeToCenter**2) < 9025000000
                if inRange and inDiameter:
                    
                    # GET PAV SETTINGS
                    verifiedElevation = myVerifiedWaferMap.get_verified_msa600_elevation_at_die(dieIndex)
                    theta = myVerifiedWaferMap.get_theta(dieIndex)

                    # GET MSA-600 SETTINGS
                    settingsFileName = myUserInput.get_settings_file(measurementIndex=measurementIndex)
                    settingsFile = os.path.join(settingsDirectory, settingsFileName)
                    myMsaAquisitionSettings = MsaAquisitionSettings(settingsDirectory, settingsFile)
                
                    # GET AWG_EXT SETTINGS
                    awgExtSettings = myUserInput.get_awg_ext_settings(measurementIndex=measurementIndex)

                    # GET SVD NAME
                    measurementName = myUserInput.get_experiment_filename(measurementIndex)
                    svdFileName = measurementName + ".svd"
                    svdFile = os.path.join(resultsDirectory, svdFileName)

                    # MOVE CHUCK TO POI
                    mySetup.myPav.move_theta(theta = theta)
                    mySetup.myPav.move_chuck_relative_to_home( -xStructureRelativeToHome, -yStructureRelativeToHome)
                    mySetup.myPav.move_probe_z(verifiedElevation) 
                    




                    # MOVE SCOPE TO EXACT POI
                    initialMsa600Coordinates = mySetup.myPav.get_probe_coordinates_relative_to_home()
                    print(initialMsa600Coordinates)
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






                    

                    ## SELECT THE TOOL SETTINGS
                    mySetup.myMsa600.change_settings(settingsFile = settingsFile)
                    mySetup.myAwgExt.change_settings (settings = awgExtSettings[0])

                    ## START MEASUREMENT 
                    mySetup.myPav.move_chuck_to_contact()

                    ## START SCAN AND SAVE RESULTS
                    mySetup.myMsa600.send_scan_request_and_trigger_awg(resultspath = svdFile, myAwgExt= mySetup.myAwgExt, timeLimitForResponse= 20, myMsaAquisitionSettings =myMsaAquisitionSettings)

                    ## DETERMINE THE RESONANCE FREQUENCY FROM THE MEASUREMENT DATA
                    # mySVD = Svd(resultsDirectory = resultsDirectory,  filename = fileNameSVD)
                    # resonananceFrequency = mySVD.get_resonance_frequency(point=1,fMin=1000000, fMax=24000000)
                    # print("resonananceFrequency: " + str(resonananceFrequency))
                    
                    ## SAVE PROCESSED MEASUREMENT DATA
                    resonananceFrequency= 19
                    measurementData = {
                        "RF": resonananceFrequency,
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

#TODO: computer vision: align: set constants
#TODO: Pumba: one line per SVD
#TODO: email polytec with error en question set settings
#TODO: remaining time estimate
#TODO: select measurements based on measurement index
#TODO: simplify code: one rule for "FOR ALL MEASUREMENTS" for loop


#TODO: computer vision: add rotation
#TODO: computer vision: autofocus
#TODO: more natural Wafermap input (1-23 in excel)
#TODO: implement multiple scan points: scan point indexes in excell file
#TODO: tutorial code sharing (first check Conda)
#TODO: Fré Quality factor for RF
