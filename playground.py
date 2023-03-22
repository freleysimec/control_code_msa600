import os
import cv2
import win32com.client
from msa_aquisition_settings_class import MsaAquisitionSettings

from post_processing.svd_class import Svd

projectLabel = "20230316_DEFN"
projectFolder = r"C:\Users\leys40\OneDrive - imec\_MEASUREMENTS\CANOPUS\20230316_DEFN"

projectDirectory = os.path.join(projectFolder)
settingsDirectory = os.path.join(projectDirectory, "msa600 settings")
settingsFileName = "noise_settings_canopus.set"
settingsFile = os.path.join(settingsDirectory, settingsFileName)




myMsaAquisitionSettings = MsaAquisitionSettings(settingsDirectory, settingsFileName)
print(myMsaAquisitionSettings.measurementPointsCount)
