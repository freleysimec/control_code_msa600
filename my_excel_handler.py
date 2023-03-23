import numpy as np
import pandas as pd
import datetime
import os


class UserInput():
    def __init__(self, projectLabel, projectDirectory):
        self.projectFile = os.path.join(
            projectDirectory, projectLabel + '.xlsx')
        self.plannedMeasurementsDf = pd.read_excel(
            self.projectFile, index_col=0, sheet_name="MEASUREMENTS")  # Pandas DataFrame
        self.toolsDf = pd.read_excel(
            self.projectFile, index_col=0, sheet_name="TOOLS")
        self.waferMapDf = pd.read_excel(
            self.projectFile, index_col=0, sheet_name="WAFER_MAP")
        self.dieMapDf = pd.read_excel(
            self.projectFile, index_col=0, sheet_name="DIE_MAP")
        self.actuationDf = pd.read_excel(
            self.projectFile, index_col=0, sheet_name="ACTUATION")

    def get_used_tools(self):
        usedTools = self.toolsDf["Your Tools"].to_numpy()
        return usedTools

    def get_wafer_map(self):
        waferMapX_np = self.waferMapDf["DieX"].to_numpy()
        waferMapY_np = self.waferMapDf["DieY"].to_numpy()
        waferMap = np.column_stack((waferMapX_np, waferMapY_np))
        return waferMap

    def get_die_size(self):
        dieSize = self.waferMapDf["SIZE"].to_numpy()[:2]
        return dieSize

    def get_measurements(self):
        return self.plannedMeasurementsDf

    def get_structure_coordinates_relative_to_die_home(self, structureIndex):
        xStructure = self.dieMapDf.at[structureIndex, 'StructureX']
        yStructure = self.dieMapDf.at[structureIndex, 'StructureY']

        structureCoordinates = [round(xStructure), round(yStructure)]
        return structureCoordinates

    def get_experiment_filename(self, experimentIndex):
        filename = str(experimentIndex)

        for column_name in self.plannedMeasurementsDf.columns[0:]:
            if column_name != "msa600 settings":
                column_data = self.plannedMeasurementsDf[column_name]
                abreviation = column_data["abreviation"]
                if not pd.notna(abreviation):
                    substring = "_" + str(column_data[experimentIndex])
                else:
                    substring = "_" + str(abreviation) + \
                        str(column_data[experimentIndex])

                filename += substring

        date = datetime.datetime.now().strftime("%Y%m%d")
        filename += "_"+date

        return filename

    def get_settings_file(self, measurementIndex):
        settingsFile = self.plannedMeasurementsDf.at[measurementIndex,
                                                     'msa600 settings']
        return settingsFile

    def get_awg_ext_settings(self, measurementIndex):
        actuationLabel = self.plannedMeasurementsDf.at[measurementIndex, 'actuation']

        if pd.notna(actuationLabel):
            actuationTypeLabel = self.actuationDf.at[actuationLabel, 'type']

            if actuationTypeLabel == "sweep":
                awgExtSettings = [{
                    "type": "sweep",
                    "voltage": self.actuationDf.at[actuationLabel, 'voltage (V)'],
                    "startFrequency": self.actuationDf.at[actuationLabel, 'start frequency (Hz)'],
                    "stopFrequency": self.actuationDf.at[actuationLabel, 'stop frequency (Hz)'],
                    "sweepTime": self.actuationDf.at[actuationLabel, 'sweep time (s)'],
                }]
            elif actuationTypeLabel == "sine":
                awgExtSettings = [{
                    "type": "sine",
                    "peakToPeakAmplitude": self.actuationDf.at[actuationLabel, 'peak to peak amplitude (V)'],
                    "frequency": self.actuationDf.at[actuationLabel, 'frequency (Hz)'],
                    "offset": self.actuationDf.at[actuationLabel, 'offset (V)'],
                }]
            elif actuationTypeLabel == "sweep_sine":
                awgExtSettings = [{
                    "type": "sweep_sine",
                    "voltage": self.actuationDf.at[actuationLabel, 'voltage (V)'],
                    "startFrequency": self.actuationDf.at[actuationLabel, 'start frequency (Hz)'],
                    "stopFrequency": self.actuationDf.at[actuationLabel, 'stop frequency (Hz)'],
                    "sweepTime": self.actuationDf.at[actuationLabel, 'sweep time (s)'],

                }, {"peakToPeakAmplitude": self.actuationDf.at[actuationLabel, 'peak to peak amplitude (V)'],
                    "frequency": 100,
                    "offset": self.actuationDf.at[actuationLabel, 'offset (V)'], },]

        return awgExtSettings


class VerifiedWaferMap():
    def __init__(self, projectLabel, projectDirectory):
        verifiedWaferName = projectLabel + "_verified_wafer"
        self.excelFile = os.path.join(
            projectDirectory, verifiedWaferName + '.xlsx')
        print("initializing verified wafermap")
        try:
            self.verifiedWaferMapDf = pd.read_excel(
                self.excelFile, index_col=0)  # Pandas DataFrame
        except:
            self.verifiedWaferMapDf = pd.DataFrame()

    def save_die_coordinates(self, index, coordinates):
        self.verifiedWaferMapDf.at[index, 'VerifiedX'] = - coordinates[0]
        self.verifiedWaferMapDf.at[index, 'VerifiedY'] = - coordinates[1]
        self.verifiedWaferMapDf.to_excel(self.excelFile, sheet_name='WAFERMAP')

    def save_theta_position(self, index, thetaPosition):
        self.verifiedWaferMapDf.at[index, 'THETA'] = thetaPosition[0]
        self.verifiedWaferMapDf.to_excel(self.excelFile, sheet_name='WAFERMAP')

    def save_msa600_elevation(self, index, elevation):
        self.verifiedWaferMapDf.at[index, 'VERIFIED_MSA_ELEVATION'] = elevation
        self.verifiedWaferMapDf.to_excel(self.excelFile, sheet_name='WAFERMAP')

    def save_die_ignored(self, index):
        self.verifiedWaferMapDf.at[index, 'VerifiedX'] = "IGNORED"
        self.verifiedWaferMapDf.at[index, 'VerifiedY'] = "IGNORED"
        self.verifiedWaferMapDf.to_excel(self.excelFile, sheet_name='WAFERMAP')

    def save_center_coordinates(self, coordinates):
        self.verifiedWaferMapDf.at[0, 'CenterX'] = - float(coordinates[0])
        self.verifiedWaferMapDf.at[0, 'CenterY'] = - float(coordinates[1])
        self.verifiedWaferMapDf.to_excel(self.excelFile, sheet_name='WAFERMAP')

    def get_coordinates_of_center_of_chuck(self):
        xCenter = self.verifiedWaferMapDf.at[0, 'CenterX']
        yCenter = self.verifiedWaferMapDf.at[0, 'CenterY']
        centerCoordinates = [xCenter, yCenter]
        return centerCoordinates

    def get_coordinates_of_die(self, dieIndex):
        xDie = self.verifiedWaferMapDf.at[dieIndex, 'VerifiedX']
        yDie = self.verifiedWaferMapDf.at[dieIndex, 'VerifiedY']
        dieCoordinates = [xDie, yDie]
        return dieCoordinates

    def get_theta(self, dieIndex):
        theta = self.verifiedWaferMapDf.at[dieIndex, 'THETA']
        return theta

    def get_verified_msa600_elevation_at_die(self, dieIndex):
        verifiedMSA600Elevation = self.verifiedWaferMapDf.at[dieIndex,
                                                             'VERIFIED_MSA_ELEVATION']
        return verifiedMSA600Elevation





class MeasurementOutput():
    def __init__(self, projectLabel, projectDirectory):
        self.excelFileUserInput = os.path.join(
            projectDirectory, projectLabel + '.xlsx')
        performedMeasurementsName = projectLabel + "_performed_measurements"
        self.excelFileMeasurements = os.path.join(
            projectDirectory, performedMeasurementsName + '.xlsx')
        self.plannedMeasurementsDf = pd.read_excel(
            self.excelFileUserInput, index_col=0, sheet_name="MEASUREMENTS")
        try:
            self.performedMeasurementsDF = pd.read_excel(
                self.excelFileMeasurements, index_col=0, sheet_name="PERFORMED")  # Pandas DataFrame
            "Found performed measurements excel file"
        except:
            self.performedMeasurementsDF = pd.read_excel(
                self.excelFileUserInput, index_col=0, sheet_name="MEASUREMENTS")
            "no performed measurements found, so empty dataframe created"

    def save_measurement_datas(self, measurementIndex, measurementData, name):
        for key in measurementData:
            measurementDataLabel = key
            measurementDataValue = measurementData[key]
            self.performedMeasurementsDF.at[measurementIndex,
                                            measurementDataLabel] = measurementDataValue
        self.performedMeasurementsDF.at[measurementIndex, 'NAME'] = name
        self.performedMeasurementsDF.to_excel(
            self.excelFileMeasurements, sheet_name='PERFORMED')

    def save_measurement_as_ignored(self, experimentIndex, message):
        self.plannedMeasurementsDf.at[experimentIndex, 'NAME'] = message
        self.plannedMeasurementsDf.to_excel(
            self.excelFileMeasurements, sheet_name='PERFORMED')

    def save_link_to_data(self, index, columnLabel, linkName, path):
        content = '=HYPERLINK("' + path + '","' + linkName + '")'
        self.performedMeasurementsDF.at[index, columnLabel] = content
        self.performedMeasurementsDF.to_excel(
            self.excelFileMeasurements, sheet_name='PERFORMED')
        return self

    def save_measurement_data(self, index, label, data):
        self.performedMeasurementsDF.at[index, label] = data
        self.performedMeasurementsDF.to_excel(
            self.excelFileMeasurements, sheet_name='PERFORMED')

    def get_flag(self, experimentIndex):
        flag = self.plannedMeasurementsDf.at[experimentIndex, 'FLAG']
        return flag
