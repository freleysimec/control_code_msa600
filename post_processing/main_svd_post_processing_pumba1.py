from pvd_class import*
from svd_class import*
from my_working_folder_class import*
import os
import sys

controlCodeDirectory = os.getcwd()
sys.path.append(controlCodeDirectory)
import my_excel_handler as myExcelHandler
import svd_methods as svdMethods



## CUSTOM 
projectLabel = "pumba1_square"
projectFolder = r"D:\pumba1_square"
pointsInSvd = 1
rfFileNameAddition = "_resonanceFrequency"
ampFileNameAddition = "_amplitude"

## INITIALISE FILES
projectDirectory = os.path.join(projectFolder)
resultsDirectory = os.path.join(projectDirectory, "results")
resultsDirectoryRelative = "results"

## INITIALISE DATA
myUserInput = myExcelHandler.UserInput(projectLabel=projectLabel, projectDirectory=projectDirectory)
myPerformedMeasurements = myExcelHandler.MeasurementOutput(projectLabel = projectLabel, projectDirectory=projectDirectory)
myPerformedMeasurementsDF = myPerformedMeasurements.performedMeasurementsDF
myResultsFolder = MyWorkingFolder(projectDirectory=projectDirectory)

print("main")
def main():    

    ## FOR ALL SVD FILES
    for index, row in myPerformedMeasurementsDF.iterrows():
        if index != "abreviation" :
            performedMeasurementName = row['NAME'] 
            if performedMeasurementName != "IGNORED STRUCTURE" and performedMeasurementName != "IGNORED" :
                
                performedMeasurementNameFrequency = performedMeasurementName + rfFileNameAddition
                performedMeasurementNameAmplitude = performedMeasurementName + ampFileNameAddition
                svdFilenameFrequency = performedMeasurementNameFrequency + ".svd"
                svdFilenameAmplitude= performedMeasurementNameAmplitude + ".svd"
                files = os.listdir(resultsDirectory)
                
                if svdFilenameFrequency in files:
                    print("index: " + str(index))
                    mySVD = Svd(resultsDirectory = resultsDirectory,  filename = svdFilenameFrequency)
                    
                    # SAVE FFT PLOT
                    svdMethods.save_fft_plot(mySVD,
                                             resultsDirectory=resultsDirectory, 
                                             resultsDirectoryRelative=resultsDirectoryRelative,
                                             columnLabel="FFT", 
                                             measurementName=performedMeasurementNameFrequency,
                                             index =index,
                                             myPerformedMeasurements=myPerformedMeasurements,
                                             )
                
                # # Get Voltage AMPLITUDE
                # if svdFilenameAmplitude in files:
                #     mySVD = Svd(resultsDirectory = resultsDirectory,  filename = svdFilenameAmplitude)
                #     myVoltages = mySVD.get_voltage(point=1)
                #     mySVD.plot_frequency_response(frequencyResponse=myVoltages)

                    # SAVE RESONANCE FREQUENCY (done at measurements)

                    # SAVE AMPLITUDE/V

                    # SAVE HEATMAP

                else:
                    print("no svd file found for measurement: " + str(index))
            # break        

if __name__ == "__main__":
    main()



