import cv2
import numpy as np
import os

def main():

    # projectFolder = r"C:\Users\leys40\OneDrive - imec\Desktop\control_code_msa600\computer_vision"
    # projectFolder = r"C:\Users\leys40\OneDrive - imec\_METINGEN\cv_test"
    projectFolder = r"D:\Fre\cv_test"
    referenceImage = "referenceImage.png"
    imageToBeTranslated = "thisDieImage.png"







    projectDirectory = os.path.join(projectFolder)
    resultsDirectory = os.path.join(projectDirectory, "results")

    imagesDirectory = os.path.join(resultsDirectory, "images")
    # read the two images
    imageLink1 = os.path.join(imagesDirectory, referenceImage)
    imageLink2 = os.path.join(imagesDirectory, imageToBeTranslated)

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

if __name__=='__main__':
    main()
    #exit()