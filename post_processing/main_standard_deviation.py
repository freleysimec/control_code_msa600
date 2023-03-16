from pvd_class import*
from svd_class import*
from my_working_folder_class import*
import os
import sys
import statistics

controlCodeDirectory = os.getcwd()
sys.path.append(controlCodeDirectory)
import my_excel_handler as myExcelHandler
import svd_methods as svdMethods



## CUSTOM 
projectLabel = "all"
projectFolder = r"D:\all"
pointsInSvd = 1

## INITIALISE FILES
projectDirectory = os.path.join(projectFolder)
resultsDirectory = os.path.join(projectDirectory, "results")
resultsDirectoryRelative = "results"

## INITIALISE DATA
myUserInput = myExcelHandler.UserInput(projectLabel=projectLabel, projectDirectory=projectDirectory)
myPerformedMeasurements = myExcelHandler.MeasurementOutput(projectLabel = projectLabel, projectDirectory=projectDirectory)
myPerformedMeasurementsDF = myPerformedMeasurements.performedMeasurementsDF
myResultsFolder = MyWorkingFolder(projectDirectory=projectDirectory)
print(myPerformedMeasurementsDF)

def main():    
    die = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
    for dieIndex in die:
        rf_die = []
        ## FOR ALL MEASUREMENTS
        for measurementIndex, row in myPerformedMeasurementsDF.iterrows():
            if measurementIndex != "abreviation" :
                performedMeasurementName = row['NAME'] 
                if performedMeasurementName != "IGNORED STRUCTURE" and performedMeasurementName != "IGNORED" :
                    
                    ## STANDARD DEVIATION : σ = √(Σ(xi - x̄)² / (n - 1)) || increases if the data points are further away from the mean and if there are less data points
                    
                    if row['die index'] == dieIndex:
                        rf_die.append(row['RF'])

                # break    
        stdev = statistics.stdev(rf_die)

        measurementData = {
            "ST DEV ALL": stdev,
        }
        measurementIndexAtStructure0 = dieIndex*10
        myPerformedMeasurements.save_measurement_datas(measurementIndexAtStructure0, measurementData)



if __name__ == "__main__":
    main()



