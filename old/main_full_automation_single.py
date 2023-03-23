import os
import time
import my_setup_class as mySetup
from post_processing.svd_class import*


#communicationDirectory = "C:\\Users\\leys40\\OneDrive - imec\\SOFTWARE\\msa600_communication\\communication_directory"
resultFrequencyFilename = 'frequencyD'
resultAmplitudeFilename = 'amplitudeD'
frequencySettingsFile = "pumba_frequency.set"
amplitudeSettingsFile = "pumba_amplitude.set"

resultsFolder = 'C:\\Users\\MMICRO\\Desktop\\control_software\\results\\'
frequencySettingsPath ='C:\\Users\\MMICRO\\Desktop\\control_software\\communication_directory\\'
amplitudeSettingsPath ='C:\\Users\\MMICRO\\Desktop\\control_software\\communication_directory\\'


def main():

    ## INITIALISE SETUP & TOOLS
    mySetup.initiate()
    # mySetup.myAwgExt.reset_config()
    time.sleep(1)

    # FOR ALL POINTS OF INTEREST

    # SELECT THE MSA-600 SETTINGS
    request = []
    # request.append("CHANGE_SETTINGS," + amplitudeSettingsPath + amplitudeSettingsFile)
    request.append("CHANGE_SETTINGS," + frequencySettingsPath + frequencySettingsFile)
    mySetup.myMsa600.send_requests(request, timeLimitForResponse= 20)

    # SELECT THE SETTINGS FOR THE VOLTAGE ACTUATION
    mySetup.myAwgExt.set_sweep_settings(startFrequency=1000, stopFrequency=25000000, sweepTime=0.028, voltage= 1)
    # mySetup.myAwgExt.set_sine_settings(peakToPeakAmplitude= 2,  frequency=9000000)

    # START SCAN AND SAVE RESULTS
    request = []
    request.append("SCAN_AND_SAVE," + resultsFolder + resultFrequencyFilename)
    mySetup.myMsa600.send_scan_request_and_trigger_awg(request, myAwgExt= mySetup.myAwgExt, timeLimitForResponse= 20)

    # DETERMINE THE RESONANCE FREQUENCY FROM THE MEASUREMENT DATA
    mySVD = Svd(resultsDirectory = resultsFolder,  filename = resultFrequencyFilename) #TODO: correct filename
    resonananceFrequency = mySVD.get_resonance_frequency(point=1,fMin=5000000, fMax=10000000)
    print("resonananceFrequency: " + str(resonananceFrequency))
    
    
    # SELECT THE MSA-600 SETTINGS
    request = []
    request.append("CHANGE_SETTINGS," + amplitudeSettingsPath + amplitudeSettingsFile)
    mySetup.myMsa600.send_requests(request, timeLimitForResponse= 20)

    # SELECT THE SETTINGS FOR THE VOLTAGE ACTUATION
    mySetup.myAwgExt.set_sine_settings(peakToPeakAmplitude= 2.5,  frequency=resonananceFrequency)
    
    # START SCAN AND SAVE RESULTS
    request = []
    request.append("SCAN_AND_SAVE," + resultsFolder + resultAmplitudeFilename)
    mySetup.myMsa600.send_scan_request_and_trigger_awg(request,  myAwgExt= mySetup.myAwgExt, timeLimitForResponse= 20)

    # PLOT VOLTAGE ACTUATION
    mySVD = Svd(resultsDirectory = resultsFolder,  filename = resultAmplitudeFilename)
    amplitudeAtResonanceFrequency = mySVD.get_amplitude_at_frequency(point = 1, frequency=resonananceFrequency)
    print("amplitudeAtResonanceFrequency: " + str(amplitudeAtResonanceFrequency))

    mySVD.plot_actuation_voltage(point=1)
    # mySVD.plot_time_velocity()


        
if __name__ == "__main__":
    main()
