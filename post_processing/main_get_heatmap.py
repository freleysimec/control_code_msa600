# FRé LEYS
# 2021-02-09
# This script is used to get a heatmap
# the links in the heatmap don't work from Sharepoint. To make them work, you have to download the projectDirectory and the resultsfolder (without the .svd files)

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook
import matplotlib.colors as colors
controlCodeDirectory = os.getcwd()
sys.path.append(controlCodeDirectory)
import my_excel_handler as myExcelHandler



### RAW DATA
projectLabel = "pumba1_circle"
projectFolder = r"D:\pumba1_circle"

columnLabel = "RF"
linkColumnLabel = "FFT"
structureIndexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
colorbarLabel = "Resonance Frequency [MHz]"
divider = 1000000
roundedTo = 1


#----------------------------------------------------
projectDirectory = os.path.join(projectFolder )
resultsDirectory = os.path.join(projectDirectory, "results")

myUserInput = myExcelHandler.UserInput(projectLabel=projectLabel, projectDirectory=projectDirectory)
myMeasurementOutput = myExcelHandler.MeasurementOutput(projectLabel = projectLabel, projectDirectory=projectDirectory)
myMeasurementsDf = myMeasurementOutput.performedMeasurementsDF
measurementsExcel = os.path.join(projectDirectory, projectLabel +"_performed_measurements.xlsx")
measurementsWb = load_workbook(filename = measurementsExcel)
sheetName = "PERFORMED"
sheet = measurementsWb[sheetName]
myMeasurementsLinksDf= pd.DataFrame(sheet.values)
myWaferMapNp = myUserInput.get_wafer_map()
myWaferMapDf = myUserInput.waferMapDf
pd.set_option('display.max_colwidth', 1000)



def main():
    
# For all structures
    for structureIndex in structureIndexes:

        # WAFERMAP to DIE_MATRIX: get size of DIE_MATRIX
        max_x_value = np.max(myWaferMapNp[:,0])
        min_x_value = np.min(myWaferMapNp[:,0])
        xSize = max_x_value - min_x_value + 1
        max_y_value = np.max(myWaferMapNp[:,1])
        min_y_value = np.min(myWaferMapNp[:,1])
        ySize = max_y_value - min_y_value + 1
        
        startData = np.nan
        # myLinkArray = np.zeros((ySize, xSize), dtype='U200')
        myLinkArray = np.full((ySize, xSize), startData, dtype='U200')
        myResonanceArray = np.full((ySize, xSize), startData)
        allMeasuredDies = np.full((ySize, xSize), True)

        ## GET DATA
        for dieIndex, die in myWaferMapDf.iterrows():


            try:
                print("dieIndex: " + str(dieIndex))

                myMeasurementsDf_filtered = myMeasurementsDf[(myMeasurementsDf['structure index'] == structureIndex) & (myMeasurementsDf['die index'] == dieIndex)]
                col_name_structure_index = myMeasurementsLinksDf.columns[myMeasurementsLinksDf.iloc[0].eq('structure index').idxmax()]
                col_name_die_index = myMeasurementsLinksDf.columns[myMeasurementsLinksDf.iloc[0].eq('die index').idxmax()]
                myMeasurementsDFLinks_filtered = myMeasurementsLinksDf[(myMeasurementsLinksDf[col_name_structure_index] == structureIndex) & (myMeasurementsLinksDf[col_name_die_index] == dieIndex)]   #TODO: adjust
                
                resonanceFrequency = myMeasurementsDf_filtered[columnLabel].iloc[0]
                name = myMeasurementsDf_filtered["NAME"].iloc[0]
                linkColumnLabelExcel = myMeasurementsLinksDf.columns[myMeasurementsLinksDf.iloc[0].eq(linkColumnLabel).idxmax()]

                linkToData = myMeasurementsDFLinks_filtered[linkColumnLabelExcel].to_string()
                start_index = linkToData.find('"') + 1
                end_index = linkToData.find('"', start_index ) 
                link = linkToData[start_index:end_index ]

                DieX = die["DieX"]
                DieY = die["DieY"]
                columnInDataMatrix = DieX - min_x_value
                rowInDataMatrix = -DieY - min_y_value
                
                x_type = type(resonanceFrequency)
                if isinstance(resonanceFrequency, x_type):
                    if (name != 'IGNORED' and name != 'IGNORED STRUCTURE'):
                        resonanceFrequency = round(float(resonanceFrequency)/divider, roundedTo)
                        myResonanceArray[rowInDataMatrix, columnInDataMatrix] = resonanceFrequency
                        myLinkArray[rowInDataMatrix, columnInDataMatrix] = link
                
                #make these dies visible
                allMeasuredDies[rowInDataMatrix,columnInDataMatrix] = False
                allMeasuredDies[rowInDataMatrix,columnInDataMatrix] = False 
            
            except:
                print("No measurement for dieIndex: " + str(dieIndex) + " and structureIndex: " + str(structureIndex) )
               


        ## PLOT
        fig, ax = plt.subplots(figsize=(8, 7))
        xSize = myUserInput.get_die_size()[0]
        ySize = myUserInput.get_die_size()[1]
        aspect = ySize/xSize

        im=ax.imshow(myResonanceArray, cmap = 'YlGnBu', aspect =aspect)
        colorbar = fig.colorbar(im)
        colorbar.set_label(colorbarLabel)


        xlabels = [str(i) for i in range(myResonanceArray.shape[1])]
        ylabels = [str(i) for i in range(myResonanceArray.shape[0])]

        reversed_yticklabels = ylabels[::-1]
        new_xticklabels = [str(int(float(label) + min_x_value)) for label in xlabels]
        new_yticklabels = [str(int(float(label) + min_y_value)) for label in reversed_yticklabels]

        ax.set_xticks(np.arange(myResonanceArray.shape[1]))
        ax.set_yticks(np.arange(myResonanceArray.shape[0]))
        ax.set_yticklabels(new_yticklabels)
        ax.set_xticklabels(new_xticklabels)

        figureTitle = projectLabel + ", Structure " + str(structureIndex) + " : " + columnLabel 
        filename = "Heatmap " + columnLabel + " Structure " + str(structureIndex) +".svg"

        ax.set_title(figureTitle)
        

        for (j,i), x in np.ndenumerate(myResonanceArray):
            x_center = i 
            y_center = j 
            url = myLinkArray[j,i]
            ax.annotate(x, xy=(x_center, y_center), ha="center", va="center",
                        url=url, bbox=dict(color='w', alpha=1e-6, url=url))

        filename = os.path.join(projectDirectory, filename)
        fig.savefig(filename, format="svg")


if __name__ == "__main__":
    main()



#TODO: put in folder called "heatmaps"