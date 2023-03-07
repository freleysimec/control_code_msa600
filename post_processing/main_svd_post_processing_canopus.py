from pvd_class import*
from svd_class import*
from my_working_folder_class import*
from PIL import Image
import my_excel_handler as myExcelHandler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


### RAW DATA
myName = "canopus"
myFolder = "C:\\Users\\leys40\\OneDrive - imec\\Gargamel 2.0\\TOOLS\\MSA-600\\Measurements\\analysis\\"
myRawDataFolder = "C:\\Users\\leys40\\OneDrive - imec\\Gargamel 2.0\\TOOLS\\MSA-600\\Measurements\\analysis\\canopus\\"  # END with \\
pointsInSvd = 10
filename = "20230217_110825_018_.svd"

### CODE ###
myWorkingFolder = MyWorkingFolder(name = myName)
userInputInstance = myExcelHandler.UserInput(myFolder = myFolder, myName = myName)
performedMeasurementsInstance = myExcelHandler.PerformedMeasurements(myFolder = myFolder, myName = myName)
performedMeasurementsDF = performedMeasurementsInstance.get_performed_measurements()
#filepath = 'canopus\\' + filename


def main():    

    ### initiations
    resonanceFrequenciesTilt = np.array([0])
    resonanceFrequenciesPiston = np.array([0])
    amplitudesTilt = np.array([0])
    amplitudesPiston= np.array([0])

    #mySVD = Svd(filePath = filepath)

    ## GET FREQUENCY, VELOCITY, DISPLACEMENT for all points
    #myFrequencyResponse = mySVD.get_frequency_response(point=pointsInSvd)

    ## PLOT FREQUENCY RESPONSE
    #mySVD.plot_frequency_response(myFrequencyResponse)

    # # GET IMAGE
    # imagingData = mySVD.get_image()
    # imageArray = imagingData['ImageArray']
    # image = Image.fromarray(imageArray)
    # image.show()


    # SAVE IMAGE FOR ALL MEASUREMENTS
    # for index, row in performedMeasurementsDF.iterrows():
    #     if index != "abreviation":
    #         performedMeasurmentIndex = row['FLAG'] 
    #         if performedMeasurmentIndex != "IGNORED STRUCTURE" and performedMeasurmentIndex != "IGNORED" :
    #             #print("performedMeasurmentIndex: " + str(performedMeasurmentIndex))
    #             svdFilename = myWorkingFolder.find_svd_file_name_based_on_performedMeasurmentIndex(int(performedMeasurmentIndex))  # the minus one is to compensate for the fact that we start measuring at 0
    #             if svdFilename != "no file found":
    #                 measurementName = userInputInstance.get_measurement_filename(index = index)
    #                 mySVD = Svd(myFolder = myRawDataFolder,  filename = svdFilename) 
                    
    #                 imagingData = mySVD.get_image()
    #                 imageArray = imagingData['ImageArray']
    #                 scanPoints = imagingData['ScanPoints']

    #                 x = scanPoints[:,0]
    #                 y = scanPoints[:,1]
    #                 # xM = scanPoints[5,0]
    #                 # yM = scanPoints[5,1]

    #                 # Display the image and the scatter plot
    #                 fig, ax = plt.subplots()
    #                 ax.imshow(imageArray, cmap='gray')
    #                 ax.scatter(x, y, s=20, c='b', marker='.')
    #                 # ax.scatter(xM, yM, s=20, c='r', marker='o')

    #                 try:
    #                     plt.savefig(myRawDataFolder + "images\\" + measurementName + '.png')
    #                 except:
    #                     folder_path = myRawDataFolder
    #                     folder_name = 'images'
    #                     full_folder_path = os.path.join(folder_path, folder_name)
    #                     os.makedirs(full_folder_path)
    #                     print("images folder created")
    #                     plt.savefig(myRawDataFolder + "images\\" + measurementName + '.png')

    #                 print("index: " + str(index))

    #             else: 
    #                 print("no svd file found for measurement: " + str(index))

    # SAVE IMAGE OVERVIEW FOR ALL MEASUREMENTS
    for index, row in performedMeasurementsDF.iterrows():
        if index != "abreviation" :
            performedMeasurmentIndexForImage = row['FLAG'] 
            if performedMeasurmentIndexForImage != "IGNORED STRUCTURE" and performedMeasurmentIndexForImage != "IGNORED" :
                performedMeasurmentIndexForData = performedMeasurmentIndexForImage -1
                svdFilenameForImage = myWorkingFolder.find_svd_file_name_based_on_performedMeasurmentName(int(performedMeasurmentIndexForImage))
                svdFilenameForData = myWorkingFolder.find_svd_file_name_based_on_performedMeasurmentName(int(performedMeasurmentIndexForData))
                
                if svdFilenameForImage != "no file found":
                    measurementName = userInputInstance.get_measurement_filename(index = index)
                    measurementName = "overview_" + measurementName 
                    mySVDForImage = Svd(resultsDirectory = myRawDataFolder,  filename = svdFilenameForImage) 
                    mySVDForData = Svd(resultsDirectory = myRawDataFolder,  filename = svdFilenameForData) 
                    
                    imagingData = mySVDForImage.get_image()
                    frequencyResponse_1 = mySVDForData.get_fft_data(point=1)
                    frequencyResponse_2 = mySVDForData.get_fft_data(point=2)
                    frequencyResponse_3 = mySVDForData.get_fft_data(point=3)
                    frequencyResponse_4 = mySVDForData.get_fft_data(point=4)
                    frequencyResponse_5 = mySVDForData.get_fft_data(point=5)
                    frequencyResponse_6 = mySVDForData.get_fft_data(point=6)
                    frequencyResponse_7 = mySVDForData.get_fft_data(point=7)
                    frequencyResponse_8 = mySVDForData.get_fft_data(point=8)
                    frequencyResponse_9 = mySVDForData.get_fft_data(point=9)
                    frequencyResponse_10 = mySVDForData.get_fft_data(point=10)



                    # for point in range(1, pointsInSvd+1):
                    #     resonananceFrequencyPiston = mySVDForData.get_resonance_frequency(point=point, fMin=7000, fMax=12000)
                    #     resonananceFrequencyTilt = mySVDForData.get_resonance_frequency(point=point,fMin=2000, fMax=6000)

                    #     performedMeasurementsInstance.save_data(index = index, label = "RF Piston " + str(point), data = resonananceFrequencyPiston)
                    #     performedMeasurementsInstance.save_data(index = index, label = "RF Tilt " + str(point), data = resonananceFrequencyTilt)



                    # plt.plot(frequencyResponse_0[0], frequencyResponse_0[1], color = 'black')
                    # plt.plot(frequencyResponse_0[0], frequencyResponse_0[1], color = 'black')


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

                    path = myRawDataFolder + "images\\" + measurementName + '.png'
                    try:
                        plt.savefig(path)
                    except:
                        folder_path = myRawDataFolder
                        folder_name = 'images'
                        full_folder_path = os.path.join(folder_path, folder_name)
                        os.makedirs(full_folder_path)
                        print("images folder created")
                        
                        plt.savefig(path)

                    relativePath =  "images\\" + measurementName + '.png'

                    performedMeasurementsInstance.save_link_to_data(index = index, label = "OVERVIEW", dataName = "image Link", path= relativePath)


                    print("index: " + str(index))


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
                    print("no svd file found for measurement: " + str(index))

            #break  #only one plot
    # print("plotting")
    # resonanceFrequenciesTilt = resonanceFrequenciesTilt[1:]
    # resonanceFrequenciesPiston = resonanceFrequenciesPiston[1:]
    # amplitudesTilt = amplitudesTilt[1:]
    # amplitudesPiston= amplitudesPiston[1:]

    # plt.scatter(resonanceFrequenciesPiston, amplitudesPiston)
    # plt.show()


    # # # FOR ALL MEASUREMENTS GET RESONANCE FREQUENCIES AND SAVE TO EXCEL

    # for index, row in performedMeasurementsDF.iterrows():
    #     if index != "abreviation":
    #         performedMeasurmentIndex = row['FLAG'] 
    #         if performedMeasurmentIndex != "IGNORED STRUCTURE" and performedMeasurmentIndex != "IGNORED" :
    #             #print("performedMeasurmentIndex: " + str(performedMeasurmentIndex))
    #             filename = myWorkingFolder.find_svd_file_name_based_on_performedMeasurmentIndex(int(performedMeasurmentIndex))  # the minus one is to compensate for the fact that we start measuring at 0
    #             if filename != "no file found":
    #                 # repeat for  i = 1 to 10
    #                 for point in range(1, pointsInSvd+1):
    #                     mySVD = Svd(filePath = 'canopus\\'+ filename)  #TODO: make this more generic
    #                     resonananceFrequencyPiston = mySVD.get_resonance_frequency(point=point, fMin=7000, fMax=12000)
    #                     resonananceFrequencyTilt = mySVD.get_resonance_frequency(point=point,fMin=2000, fMax=6000)

    #                     performedMeasurements.save_data(index = index, label = "RF Piston " + str(point), data = resonananceFrequencyPiston)
    #                     performedMeasurements.save_data(index = index, label = "RF Tilt " + str(point), data = resonananceFrequencyTilt)
                        
    #                     print("performedMeasurmentIndex: " + str(performedMeasurmentIndex))
    #             else: 
    #                 print("no svd file found for measurement: " + str(performedMeasurmentIndex))
    #                 performedMeasurements.save_data(label = "RF", data = "NA", index = index)



if __name__ == "__main__":
    main()


#TODO: now only for 1 point: we need 10 points
#TODO: have a max for all frequencies.. but how to know if wrong...: find average, compare max value with average
#TODO: heatmap
#TODO: date of experiment in performed measurements excel