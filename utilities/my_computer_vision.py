
import os
import time
from post_processing.svd_class import*
import my_methods as myMethods
import cv2
import numpy as np

def take_and_save_reference_image(imagesDirectory, mySetup):
    communicationDirectory = "msa600_macros" #where msa600 settings for image taking is saved

    # SELECT THE MSA-600 SETTINGS
    settingsPath = os.path.join(communicationDirectory)
    requests = ["CHANGE_SETTINGS," + str(settingsPath)]
    mySetup.myMsa600.send_requests(requests, timeLimitForResponse= 20)

    # START SCAN AND SAVE RESULTS
    fileNameSVD = "referenceImage.svd"
    resultspath = os.path.join(imagesDirectory, fileNameSVD)
    requests = ["SCAN_AND_SAVE," + str(resultspath)]
    mySetup.myMsa600.send_requests(requests, timeLimitForResponse= 20)

    # SAVE REFERENCE IMAGE
    mySVD = Svd(resultsDirectory = imagesDirectory,  filename = fileNameSVD)
    imagingData = mySVD.get_image()
    imageArray = imagingData['ImageArray']
    image = Image.fromarray(imageArray)
    filename_without_ext = os.path.splitext(fileNameSVD)[0]
    imageInImagesDirectory = os.path.join(imagesDirectory, filename_without_ext +'.png')
    image.save(imageInImagesDirectory)  

def take_and_save_image(imagesDirectory, imageName, mySetup):
    communicationDirectory = "msa600_macros" #where msa600 settings for image taking is saved

    # SELECT THE MSA-600 SETTINGS
    settingsPath = os.path.join(communicationDirectory)
    requests = ["CHANGE_SETTINGS," + str(settingsPath)]
    mySetup.myMsa600.send_requests(requests, timeLimitForResponse= 20)

    # START SCAN AND SAVE RESULTS
    fileNameSVD = imageName + ".svd"
    resultspath = os.path.join(imagesDirectory, fileNameSVD)
    requests = ["SCAN_AND_SAVE," + str(resultspath)]
    mySetup.myMsa600.send_requests(requests, timeLimitForResponse= 20)

    # SAVE REFERENCE IMAGE
    mySVD = Svd(resultsDirectory = imagesDirectory,  filename = fileNameSVD)
    imagingData = mySVD.get_image()
    imageArray = imagingData['ImageArray']
    image = Image.fromarray(imageArray)
    filename_without_ext = os.path.splitext(fileNameSVD)[0]
    imageInImagesDirectory = os.path.join(imagesDirectory, filename_without_ext +'.png')
    image.save(imageInImagesDirectory)  

def get_translation_between_myImage_and_reference_image(imagesDirectory, myImage, referenceImageName = "referenceImage.png"):

    imageLink1 = os.path.join(imagesDirectory, referenceImageName)
    imageLink2 = os.path.join(imagesDirectory, myImage)

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
                





