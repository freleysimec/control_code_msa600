import my_excel_handler as myExcelHandler
import time
import pandas as pd
import numpy as np
import keyboard as keyboard
import my_setup as mySetup
import os
import sys
import numpy as np
from post_processing.svd_class import*
import my_methods as myMethods


projectLabel = "cv_test"
projectFolder = r"C:\Users\MMICRO\Desktop\control_software\cv_test"
averaging = 1

## INITIALISE FILES
projectDirectory = os.path.join(projectFolder)
resultsDirectory = projectDirectory
imagesDirectory = os.path.join(projectDirectory, "images")
if not os.path.exists(projectDirectory):
    print("Can't find project directory: " + projectDirectory)
    sys.exit()
if not os.path.exists(imagesDirectory):
    os.makedirs(imagesDirectory)




## INITIALISE SETUP & TOOLS
mySetup.initiate()
time.sleep(1)
mySetup.myPav.move_chuck_to_contact()




# MOVE SCOPE TO EXACT POSITION

# take current coordinates of scope
initialMsa600Coordinates = mySetup.myPav.get_probe_coordinates_relative_to_home()
print("probeCoordinates: " + str(initialMsa600Coordinates))

# take fast svg 
fileNameSVD = "otherImage.svd"
resultspath = os.path.join(resultsDirectory, fileNameSVD)
requests = ["SCAN_AND_SAVE," + str(resultspath)]
mySetup.myMsa600.send_scan_request_and_trigger_awg(requests, myAwgExt= mySetup.myAwgExt, timeLimitForResponse= 20, averageCount = averaging, triggerOpenTime=1)

# get position image from scope
mySVD = Svd(resultsDirectory = projectDirectory,  filename = fileNameSVD)
imagingData = mySVD.get_image()
imageArray = imagingData['ImageArray']
image = Image.fromarray(imageArray)
filename_without_ext = os.path.splitext(fileNameSVD)[0]
imageInImagesDirectory = os.path.join(imagesDirectory, filename_without_ext +'.png')
image.save(imageInImagesDirectory)   

# get translation values
translation = myMethods.get_translation_between_two_images(imagesDirectory= imagesDirectory,  referenceImageName="centered_focussed.png", otherImage= "otherImage.png")
print("translation: "+str(translation))

# move MSA to new position
newXcoord = float(initialMsa600Coordinates[1]) -translation[0]
newYcoord = float(initialMsa600Coordinates[2]) - translation[1]
mySetup.myPav.move_probe_relative_to_home(x = newXcoord, y =newYcoord)

