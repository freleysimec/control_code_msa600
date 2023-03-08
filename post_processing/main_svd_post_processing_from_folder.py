from svd_class import*
from my_working_folder_class import*
import time
import os
import sys
controlCodeDirectory = os.getcwd()
sys.path.append(controlCodeDirectory)
import svd_methods as svdMethods

## CUSTOM 
projectFolder = r"C:\Users\leys40\OneDrive - imec\Desktop\control_code_msa600\computer_vision"
pointsInSvd = 1

## INITIALISE FILES
projectDirectory = os.path.join(projectFolder)
imagesDirectory = os.path.join(projectDirectory, "images")
if not os.path.exists(imagesDirectory):
    os.makedirs(imagesDirectory)
def main():    

    ## FOR ALL SVD FILES IN FOLDER
    files = os.listdir(projectDirectory)
    for file in files:
        if os.path.isfile(os.path.join(projectDirectory, file)):
            filename = os.fsdecode(file)
            print(filename)
            mySVD = Svd(resultsDirectory = projectDirectory,  filename = filename)
            imagingData = mySVD.get_image()
            imageArray = imagingData['ImageArray']
            image = Image.fromarray(imageArray)
            filename_without_ext = os.path.splitext(filename)[0]
            imageInImagesDirectory = os.path.join(imagesDirectory, filename_without_ext +'.png')
            image.save(imageInImagesDirectory)   

if __name__ == "__main__":
    main()



