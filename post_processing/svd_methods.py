import os
from svd_class import*
from my_excel_handler import*

def save_fft_plot(mySVD: Svd, 
                  resultsDirectory, 
                  resultsDirectoryRelative, 
                  measurementName, 
                  columnLabel,
                  index, 
                  myPerformedMeasurements: MeasurementOutput):
    
    frequencyResponse = mySVD.get_fft_data(point=1)
    plt.plot(frequencyResponse[0], frequencyResponse[1], color = 'black')

    graphsDirectory = os.path.join(resultsDirectory, "graphs") 
    graphsDirectoryRelative = os.path.join(resultsDirectoryRelative, "graphs") 
    graphName = measurementName + '.png'
    relativePath = os.path.join(graphsDirectoryRelative, graphName) 
    graphNameAndPath = os.path.join(graphsDirectory, graphName)

    try:
        plt.savefig(graphNameAndPath)
    except:
        os.makedirs(graphsDirectory)
        print("graphs folder created")
        plt.savefig(graphNameAndPath)
    
    plt.close()

    myPerformedMeasurements.save_link_to_data(index = index, columnLabel = columnLabel, linkName = "graph Link", path= relativePath)