import datetime
import numpy as np
from scipy import signal

## GENERAL
mainFolder =  "C:\\Users\\Gargamel\\Desktop\\software_v3\\"
waferName = "CANOPUS"
waferID = "D01"              #  use correct format! example: D06
#structureID = "S06_ID01"     # use correct format! example: S06_ID01
#measurementType = "DV"       # use correct format! example: DV

## WAFER
dieSizeX = 21760
dieSizeY = 21760
wafermapFolder = mainFolder + "wafermaps\\"
dieMap = wafermapFolder + "die_map_canopus.csv"
waferMap = wafermapFolder + "wafer_map_canopus.csv"

## MEASUREMENTS
measurementResultfileName = "myMeasurements"
myMeasurementsToBeConducted = {
                'PE_K2612B': False,
                'PE_K4200': False,
                'CV': False,
                'DV': True,
                'FR': False,
                'MAPPING': False,
                'PICTURE': False
                 }

## DV-Measurements
dvVoltages = [50]
dvAmpGain = 50
dvRepeats = 1
msvInputData = {'msv_sweep_dv_settings_file': 'D:\\Lifetime_Capella\\Settings_e31f_8.set',
            'msv_sweep_fr_settings_file': 'D:\\Lifetime_Capella\\Settings_resonance.set',
            'msv_results_folder': 'D:\\' + waferName + '\\' + datetime.datetime.now().strftime("%Y%m%d")+'\\'} 

scopePositionX = -1371    #TODO: redo this: think about way we can set (probe) & polytec position in a more general way relative to die marker. 
scopePositionY = -3105

## DV - MEASUREMENTS with NI USB 6363: actuation voltage signal: a symtercial Saw Tooth Signal
frequencyDV = 22
amplitudeDV = 0.4             # 0.4x 50 => 20V
peakToPeakAmplitudeDV = 2* amplitudeDV
amountOfPeriodsDV = 6         # amount of teeth
sampelsPerPeriodDV = 1000     # samples per tooth

t = np.linspace(0, amountOfPeriodsDV/frequencyDV, sampelsPerPeriodDV *amountOfPeriodsDV)          #time vector

writeSampleRate = frequencyDV*sampelsPerPeriodDV
nWriteSamples = sampelsPerPeriodDV*amountOfPeriodsDV
readSampleRate = writeSampleRate
nReadSamples = nWriteSamples  #for plot need to be the same

symmetricalSawTooth = amplitudeDV* signal.sawtooth(2*np.pi*frequencyDV*t+np.pi/2, width=0.5)
symmetricalSawTooth[0:10] = 0
symmetricalSawTooth[nWriteSamples-10:nWriteSamples] = 0

voltageActuationSignalDV = symmetricalSawTooth

triggerSignal = np.ones(nWriteSamples, dtype=bool)
triggerSignal[0] = False

## FR - MEASUREMENTS with NI USB 6363: actuation voltage signal: a frequency sweep
sweepTime = 3
writeSampleRateRF = 10000                                   # DV:22000
nWriteSamplesRF = sweepTime*writeSampleRateRF                      # DV: 6000
readSampleRateRF = writeSampleRateRF
nReadSamplesRF = nWriteSamplesRF  #for plot need to be the same

tFR = np.linspace(0, sweepTime, nWriteSamplesRF)[5:]
startFrequency = 100
stopFrequency = 4000
frequencySweep = 0.02*signal.chirp(tFR, startFrequency, sweepTime, stopFrequency, method='linear', phi=0, vertex_zero=True)

voltageActuationSignalFR = frequencySweep

# LOGGING
def setLogFileName():
    global waferMap
    #get date in the format YYYYMMDD
    date = datetime.datetime.now().strftime("%Y%m%d")

    fileName = date+"_"+waferID+"_logFile.txt"
    print(fileName)
    return fileName

logFileName = setLogFileName()
logFilePath= mainFolder + logFileName


#TODO: maybe better is to make a class "my_wafer"  



