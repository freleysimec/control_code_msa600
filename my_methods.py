import my_setup as mySetup
import my_excel_handler as myExcelHandler
import os
import numpy as np
import cv2




def save_coordinates_and_msa600_elevation_semi_auto(dieIndex, myVerifiedWaferMap: myExcelHandler.VerifiedWaferMap):
    textInput = input("Enter 't' if Coordinates and Focus are OK or 'i' to ignore the die: ")

    if(textInput == 't'):
        print('saving coordinates & focus elevation')
        chuckCoordinates = mySetup.myPav.get_chuck_coordinates()
        probeCoordinates = mySetup.myPav.get_probe_coordinates_relative_to_home()  #MSA Attached to "Probe station"
        x = float(chuckCoordinates[0])
        y = float(chuckCoordinates[1])
        msa600_elevation = float(probeCoordinates[3])           #MSA Attached to "Probe station"
        #save coordinates
        print('index: ' +str(dieIndex))
        myVerifiedWaferMap.save_die_coordinates(index= dieIndex, coordinates=[x,y])
        myVerifiedWaferMap.save_msa600_elevation(index= dieIndex, elevation = msa600_elevation)
    elif(textInput == 'i'):
        print('ignored die')
        #save coordinates
        print('index: ' +str(dieIndex))
        myVerifiedWaferMap.save_die_coordinates(index= dieIndex, coordinates=["IGNORED","IGNORED"])

def save_coordinates_and_msa600_elevation_manual(myVerifiedWaferMap: myExcelHandler.VerifiedWaferMap):
    textInput = input("Enter 't' if Coordinates and Focus are OK or 'f' to finish: ")

    if(textInput == 't'):
        dieIndex = input("Enter the name (index) for the die you are taking the coordinates of and press enter: ")
        print('saving coordinates & focus elevation')
        chuckCoordinates = mySetup.myPav.get_chuck_coordinates()
        probeCoordinates = mySetup.myPav.get_probe_coordinates_relative_to_home()
        x = float(chuckCoordinates[0])
        y = float(chuckCoordinates[1])
        msa600_elevation = float(probeCoordinates[3])        
        #save coordinates
        print('index: ' +str(dieIndex))
        myVerifiedWaferMap.save_die_coordinates(index= dieIndex, coordinates=[x,y])
        myVerifiedWaferMap.save_msa600_elevation(index= dieIndex, elevation = msa600_elevation)
        return False
    elif(textInput == 'f'):
        return True

def anotate_die_ignored(dieIndex, myVerifiedWaferMap: myExcelHandler.VerifiedWaferMap):
    myVerifiedWaferMap.save_die_ignored(index= dieIndex)

def get_and_save_coordinates_of_center_of_chuck(myVerifiedWaferMap: myExcelHandler.VerifiedWaferMap):
    chuckCoordinates = mySetup.myPav.get_chuck_coordinates()
    myVerifiedWaferMap.save_center_coordinates(coordinates=chuckCoordinates)
    x = float(chuckCoordinates[0])
    y = float(chuckCoordinates[1])
    return [x,y]

def get_translation_between_two_images(imagesDirectory, referenceImage, otherImage):

    imageLink1 = os.path.join(imagesDirectory, referenceImage)
    imageLink2 = os.path.join(imagesDirectory, otherImage)

    img1 = cv2.imread(imageLink1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(imageLink2, cv2.IMREAD_GRAYSCALE)

    # create a feature detector and descriptor
    orb = cv2.ORB_create()

    # detect and compute keypoints and descriptors for both images
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # create a feature matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # match the descriptors of the two images
    matches = bf.match(des1, des2)

    # sort the matches by distance
    matches = sorted(matches, key=lambda x: x.distance)

    # extract the coordinates of the matching keypoints
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # estimate the affine transform between the two images
    M, _ = cv2.estimateAffinePartial2D(pts1, pts2)

    # extract the translation from the affine transform matrix
    tx = M[0, 2]
    ty = M[1, 2]

    tx = -(27.9/17.1399692869)*tx
    ty = (59/29.952928129)*ty

    print("Translation between the two images: ({}, {})".format(tx, ty))
    return [tx,ty]
                

