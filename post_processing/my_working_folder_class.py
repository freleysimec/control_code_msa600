import os

class MyWorkingFolder:
    def __init__(self, projectDirectory):
        self.workingFolder = projectDirectory + "results\\"
        print(self.workingFolder)

    def find_svd_file_name_based_on_performedMeasurmentName(self, performedMeasurementName):
        filename = "no file found"
        performedMeasurementsFilenames = os.listdir(self.workingFolder)
        performedMeasurementsFilenames = [f for f in performedMeasurementsFilenames if os.path.isfile(os.path.join(self.workingFolder, f))]

        filetypeMeasurementFiles = [item.split(".")[1] for item in performedMeasurementsFilenames]
        
        for index, item in enumerate(performedMeasurementsFilenames):
            if filetypeMeasurementFiles[index] ==  "svd":
                performedMeasurementsIndexesInFileNameString = item.split("_")[2]
                performedMeasurementsIndexesInFileNameInt = int(performedMeasurementsIndexesInFileNameString)
                if performedMeasurementsIndexesInFileNameInt  == performedMeasurementName:
                    filename = performedMeasurementsFilenames[index]
        return filename
