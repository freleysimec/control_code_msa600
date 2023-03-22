from win32com.client import Dispatch
import os
import inspect


class MsaAquisitionSettings:
    def __init__(self, settingsDirectory, filename):
        self.filePath = os.path.join(settingsDirectory, filename)
        self.polytecFile = Dispatch('PolyFile.PolyFile')
        self.polytecFile.open(self.filePath)
        self.info = self.polytecFile.Infos

        # AVERAGE PROPERTIES
        self.hasAverageProperties = self.info.AcquisitionInfoModes.ActiveProperties.HasAverageProperties
        if(self.hasAverageProperties):
            self.averageCount = self.info.AcquisitionInfoModes.ActiveProperties.AverageProperties.Count
            type = self.info.AcquisitionInfoModes.ActiveProperties.AverageProperties.Type
            typeLibrary = {
            0: 'Averaging is off.',
            1: 'Magnitude averaging.',
            2: 'Complex averaging.',
            3: 'Time mode averaging.',
            4: 'Peak Hold averaging.',
            }
            self.averageType = typeLibrary[type] 
        else:
            print("no GeneralProperties")

        # FFT PROPERTIES
        self.hasFftProperties = self.info.AcquisitionInfoModes.ActiveProperties.HasFftProperties
        if(self.hasFftProperties):
            self.startFrequency = self.info.AcquisitionInfoModes.ActiveProperties.FftProperties.StartFrequency
            self.endFrequency = self.info.AcquisitionInfoModes.ActiveProperties.FftProperties.EndFrequency
            self.sampleFrequency = self.info.AcquisitionInfoModes.ActiveProperties.FftProperties.SampleFrequency
            self.sampleTime = self.info.AcquisitionInfoModes.ActiveProperties.FftProperties.SampleTime
            self.fftLines = self.info.AcquisitionInfoModes.ActiveProperties.FftProperties.Lines
            self.bandWidth = self.info.AcquisitionInfoModes.ActiveProperties.FftProperties.BandWidth
            self.usedSamples = self.info.AcquisitionInfoModes.ActiveProperties.FftProperties.Samples
        else:
            print("no FftProperties")

        # TRIGGER PROPERTIES
        self.hasTriggerProperties = self.info.AcquisitionInfoModes.ActiveProperties.HasTriggerProperties
        if(self.hasTriggerProperties):
            source = self.info.AcquisitionInfoModes.ActiveProperties.TriggerProperties.Source
            sourceLibrary = {
            0: 'The trigger source is analog.',
            1: 'The trigger source is external.',
            2: 'The trigger source is internal.',
            3: 'The trigger source is off.',
            }
            self.source = sourceLibrary[source]
        else:
            print("no TriggerProperties")

         # AMOUNT OF MEASUREMENT POINTS        
        if(self.info.HasMeasPoints): 
            self.measurementPointsCount = self.info.MeasPoints.Count
        else:
            print("no MeasPoints")

    def create_overview_file(self, settingsDirectory = "settings", filename = 'settings_overview.txt'):

        if not os.path.exists(settingsDirectory):
            os.makedirs(settingsDirectory)    

        file = os.path.join(settingsDirectory, filename)

        with open(file, 'w') as f:
            # Write class name
            f.write(f"Class: {self.__class__.__name__}\n\n")

            # Write members and their values
            f.write("Members:\n")
            for name, value in self.__dict__.items():
                f.write(f"  {name}: {value}\n")
