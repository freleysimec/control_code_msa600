## FRE LEYS JAN 2023
import time
import my_setup_class as mySetup
import my_excel_handler as myExcelHandler

filename = "canopus"
averagingAmount = 20
sampleTime = 4     #s
delay = 7               #s


### NO TOUCHY TOUCHY
filenameVerifiedWafer = filename +"_verified_wafer"
filenamePerformedMeasurements = filename +"_performed_measurements"

def main():

    ## INITIALISE SETUP & TOOLS
    mySetup.initiate()
    # mySetup.mySwi.open_all_switches()
    # mySetup.myAwg.reset_config()

    ## INITIALISE USER INPUT & WAFERMAP
    myUserInput = myExcelHandler.UserInput(filename)
    myVerifiedWaferMap = myExcelHandler.VerifiedWaferMap(filenameVerifiedWafer)
    myVerifiedWaferMapCoordinates = myVerifiedWaferMap.get_verified_coordinates()
    myVerifiedWaferMapCoordinates = myVerifiedWaferMap.get_verified_coordinates()
    myVerifiedMsa600Elevation = myVerifiedWaferMap.get_verified_msa600_elevation()
    myMeasurementOutput = myExcelHandler.MeasurementOutput(excelFilePlannedMeasurements = filename, excelFilePerformedMeasurements = filenamePerformedMeasurements)

    ## INITIATE MEASUREMENT
    #mySetup.mySwi.close_ext_awg()   # triggers MSA-600 || only when Switch is used
    mySetup.myPav.move_chuck_separation()
    nameOfMSA600Filename = 1
    centerCoordinates = myVerifiedWaferMap.get_coordinates_of_center_of_chuck()
    xCenter = centerCoordinates[0]
    yCenter = centerCoordinates[1]
    pavXMin = -76350
    pavXMax = 76680
    pavYMin = -76520
    pavYMax = 74970

    ## FOR ALL EXPERIMENTS
    myExperiments = myUserInput.get_measurements()
    for measurementIndex, experiment in myExperiments.iterrows():
        
        if not measurementIndex == "abreviation":    
            initialTime = time.time()

            # MOVE CHUCK TO POI IF DIE NOT IGNORED
            dieIndexAsInt = int(experiment["die index"])
            dieCoordinates = myVerifiedWaferMapCoordinates[dieIndexAsInt]
            verifiedElevation = myVerifiedMsa600Elevation[dieIndexAsInt]
            print("verifiedElevation: "+ str(verifiedElevation))
            if not dieCoordinates[0] == "IGNORED":
                
                #get structure coordinates
                structureIndexAsInt = int(experiment["structure index"])
                structureCoordinatesRelativeToDie = myUserInput.get_structure_coordinates_relative_to_die_home(structureIndexAsInt)
                
                xStructureRelativeToCenter = dieCoordinates[0] + xCenter + structureCoordinatesRelativeToDie[0]
                yStructureRelativeToCenter = dieCoordinates[1] + yCenter + structureCoordinatesRelativeToDie[0]
                xStructureRelativeToHome = dieCoordinates[0] + structureCoordinatesRelativeToDie[0]
                yStructureRelativeToHome = dieCoordinates[1] + structureCoordinatesRelativeToDie[1]

                print(xStructureRelativeToHome)
                print(yStructureRelativeToHome)
                #if structure in range
                inRange = xStructureRelativeToCenter > pavXMin and xStructureRelativeToCenter < pavXMax and yStructureRelativeToCenter > pavYMin and yStructureRelativeToCenter < pavYMax
                inDiameter = (xStructureRelativeToCenter**2 + yStructureRelativeToCenter**2) < 9025000000
                if inRange and inDiameter:
                
                    # Move chuck to sum of die AND structure coordinates (opgelet, verified wafer is chuck coordinates en structure coordinates tegengestelde assen)
                    mySetup.myPav.move_chuck_relative_to_home( -xStructureRelativeToHome, -yStructureRelativeToHome)

                    # Move MSA-600 to focus height
                    mySetup.myPav.move_probe_z(verifiedElevation) 

                    # PERFORM MEASUREMENT 
                    print("x postion: " + str(dieCoordinates[0]))
                    print("y postion: " + str(dieCoordinates[1]))
                    mySetup.myPav.move_chuck_to_contact()

                    mySetup.myAwgExt.awg_trigger(averagingAmount*sampleTime + 1)
                    time.sleep(delay) #TODO: this sleep time should be long enough! So that previous measurement is certainly finished (no feedback from MSA600)

                    # # Repeat to average
                    # for i in range(averagingAmount):
                    #     mySetup.myAwgExt.awg_trigger_dv()
                    #     time.sleep(sampleTime + 1)


                    ## TIME ESTIMATE
                    measurementTimeOneExperiment = time.time()-initialTime
                    print("estimated time 1 experiment (s): " + str(measurementTimeOneExperiment))
                    estimatedTotalTime = measurementTimeOneExperiment* len(myExperiments.index)
                    print("estimatesd total time (m): " + str(estimatedTotalTime/60))

                    ## SAVE performed measurement in "measurements done file" (links measurement number with MSA600 file number)
                    myMeasurementOutput.save_measurement(measurementIndex, nameOfMSA600Filename)
                    nameOfMSA600Filename += 1
                
                else:
                    print("measurement Ignored because Structure not in Range")
                    ## SAVE performed measurement in "measurements done file" (anotate IGNORED under DIE)
                    myMeasurementOutput.save_measurement(measurementIndex, "IGNORED STRUCTURE")

            else:
                print("measurement Ignored because Die not in Range")
                ## SAVE performed measurement in "measurements done file" (anotate IGNORED under DIE)
                myMeasurementOutput.save_measurement(measurementIndex, "IGNORED")


            ## TAKE PICTURE
            #experimentFileName = myUserInput.get_experiment_filename(experimentIndex = experimentIndex)
            #mySetup.myCamera.take_printscreen(experimentFileName)      #better picture in .PSV data!
    
    ## FINISH THE MEASUREMENTS    
    mySetup.myPav.move_chuck_separation()
    mySetup.myPav.move_chuck_relative_to_home(0,0)
    print('Experiments finished')

if __name__=='__main__':
    main() 
    #exit()


# TODO:
# - save Index of measurement somewhere to compare with filename of MSA files