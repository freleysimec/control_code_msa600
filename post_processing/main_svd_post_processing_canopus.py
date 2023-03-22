from my_working_folder_class import*
import matplotlib.pyplot as plt
import os
import sys
controlCodeDirectory = os.getcwd()
sys.path.append(controlCodeDirectory)
import my_excel_handler as myExcelHandler
from svd_class import*


projectLabel = "20230316_DEFN"
projectFolder = r"C:\Users\leys40\OneDrive - imec\_MEASUREMENTS\CANOPUS\20230316_DEFN"
points = 10


## INITIALISE FILES
# controlCodeDirectory = os.getcwd()
projectDirectory = os.path.join(projectFolder)
resultsDirectory = os.path.join(projectDirectory, "results")
settingsDirectory = os.path.join(projectDirectory, "msa600 settings")
imagesDirectory = os.path.join(resultsDirectory, "images")

if not os.path.exists(projectDirectory):
    print("Can't find project directory: " + projectDirectory)
    sys.exit()
if not os.path.exists(resultsDirectory):
    print("Can't find results directory: " + resultsDirectory)
if not os.path.exists(imagesDirectory):
    os.makedirs(imagesDirectory)

## INITIALISE DATA
myUserInput = myExcelHandler.UserInput(projectLabel=projectLabel, projectDirectory=projectDirectory)
myPerformedMeasurements = myExcelHandler.MeasurementOutput(projectLabel = projectLabel, projectDirectory=projectDirectory)
myPerformedMeasurementsDF = myPerformedMeasurements.performedMeasurementsDF
myResultsFolder = MyWorkingFolder(projectDirectory=projectDirectory)


def main():    

    ## FOR ALL SVD FILES
    for measurementIndex, row in myPerformedMeasurementsDF.iterrows():
        if measurementIndex != "abreviation" :
            performedMeasurementName = row['NAME'] 
            if performedMeasurementName != "IGNORED STRUCTURE" and performedMeasurementName != "IGNORED" :
              
                svdFilename = performedMeasurementName + ".svd"
                files = os.listdir(resultsDirectory)

                if svdFilename in files:
                    print("index: " + str(measurementIndex))
                    mySVD = Svd(resultsDirectory = resultsDirectory,  filename = svdFilename)
                    
                    imagingData = mySVD.get_image()
                    frequencyResponse_1 = mySVD.get_fft_data(point=1)
                    frequencyResponse_2 = mySVD.get_fft_data(point=2)
                    frequencyResponse_3 = mySVD.get_fft_data(point=3)
                    frequencyResponse_4 = mySVD.get_fft_data(point=4)
                    frequencyResponse_5 = mySVD.get_fft_data(point=5)
                    frequencyResponse_6 = mySVD.get_fft_data(point=6)
                    frequencyResponse_7 = mySVD.get_fft_data(point=7)
                    frequencyResponse_8 = mySVD.get_fft_data(point=8)
                    frequencyResponse_9 = mySVD.get_fft_data(point=9)
                    frequencyResponse_10 = mySVD.get_fft_data(point=10)



                    for point in range(1, points+1):
                        resonananceFrequencyPiston = mySVD.get_resonance_frequency(point=point, fMin=7000, fMax=12000)
                        resonananceFrequencyTilt = mySVD.get_resonance_frequency(point=point,fMin=2000, fMax=6000)
                        
                        measurementData = {
                            "RF Piston " + str(point): resonananceFrequencyPiston,
                            "RF Tilt " + str(point): resonananceFrequencyTilt,
                        }
                        
                        myPerformedMeasurements.save_measurement_datas(measurementIndex, measurementData, name=performedMeasurementName)


                    imageArray = imagingData['ImageArray']
                    scanPoints = imagingData['ScanPoints']

                    x = scanPoints[:,0]
                    x_odd = x[1::2]

                    y = scanPoints[:,1]
                    y_odd = y[1::2]

                    xM = scanPoints[8,0]
                    yM = scanPoints[9,1]

                    # Display the image and the scatter plot
                    fig, ax = plt.subplots(nrows=3, ncols=3)
                    ax[0, 0].imshow(imageArray, cmap='gray')
                    ax[0, 0].scatter(x, y, s=20, c='r', marker='.')
                    ax[0, 0].scatter(x_odd, y_odd, s=20, c='b', marker='.')
                    #ax[0, 0].set_ylim([0, 1.5*10**-9])

                    # center
                    ax[1, 1].plot(frequencyResponse_1[0], frequencyResponse_1[1], color = 'r')
                    ax[1, 1].plot(frequencyResponse_2[0], frequencyResponse_2[1], color = 'b')
                    ax[1, 1].set_ylim([0, 2*10**-9])
                    #ax[1, 1].ylim(0, 6)
                    

                    # top
                    ax[0, 1].plot(frequencyResponse_5[0], frequencyResponse_5[1], color = 'r')
                    ax[0, 1].plot(frequencyResponse_6[0], frequencyResponse_6[1], color = 'b')
                    ax[0, 1].set_ylim([0, 2*10**-9])

                    #bottom
                    ax[2, 1].plot(frequencyResponse_9[0], frequencyResponse_9[1], color = 'r')
                    ax[2, 1].plot(frequencyResponse_10[0], frequencyResponse_10[1], color = 'b')
                    ax[2, 1].set_ylim([0, 2*10**-9])

                    #left
                    ax[1, 0].plot(frequencyResponse_3[0], frequencyResponse_3[1], color = 'r')
                    ax[1, 0].plot(frequencyResponse_4[0], frequencyResponse_4[1], color = 'b')
                    ax[1, 0].set_ylim([0, 2*10**-9])

                    #right
                    ax[1, 2].plot(frequencyResponse_7[0], frequencyResponse_7[1], color = 'r')
                    ax[1, 2].plot(frequencyResponse_8[0], frequencyResponse_8[1], color = 'b')
                    ax[1, 2].set_ylim([0, 2*10**-9])

                    path = os.path.join(imagesDirectory, performedMeasurementName + '.png')
                    plt.savefig(path)

                    relativePath =  "results\\" + "images\\" + performedMeasurementName + '.png'

                    myPerformedMeasurements.save_link_to_data(index = measurementIndex, columnLabel = "OVERVIEW", linkName = "image Link", path= relativePath)

                    # #SCATTER PLOT RESONANCE FREQUENCY for only choosen measurements
                    # if row['score 1'] == 1  : 
                    #     # for all points from 1 to 10
                    #     for point in range(1,11):
                    #         resonanceFrequencyTilt = mySVDForData.get_resonance_frequency(point=point, fMin = 2000, fMax=5000)
                    #         resonanceFrequencyPiston = mySVDForData.get_resonance_frequency(point=point, fMin = 7000, fMax=12000)
                    #         amplitudeAtResonanceFrequencyTilt = mySVDForData.get_amplitude_at_frequency( point = point, frequency = resonanceFrequencyTilt)
                    #         amplitudeAtResonanceFrequencyPiston = mySVDForData.get_amplitude_at_frequency( point = point, frequency = resonanceFrequencyPiston)
                    #         resonanceFrequenciesTilt = np.append(resonanceFrequenciesTilt, resonanceFrequencyTilt)
                    #         resonanceFrequenciesPiston = np.append(resonanceFrequenciesPiston, resonanceFrequencyPiston)
                    #         amplitudesTilt = np.append(amplitudesTilt, amplitudeAtResonanceFrequencyTilt)
                    #         amplitudesPiston = np.append(amplitudesPiston, amplitudeAtResonanceFrequencyPiston)

                else: 
                    print("no svd file found for measurement: " + str(measurementIndex))

            # break  #only one plot


if __name__ == "__main__":
    main()