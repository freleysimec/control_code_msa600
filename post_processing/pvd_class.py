from win32com.client import Dispatch
import numpy as np
import my_plotter_methods as myPlotter
import io
from PIL import Image


class Pvd:
    def __init__(self, filename):
        filePath = "C:\\Users\\leys40\\OneDrive - imec\\Gargamel 2.0\\TOOLS\\MSA-600\\Measurements\\analysis\\my_experiments\\"
        filePath = filePath+filename
        self.filePath = filePath
        self.polytecFile = Dispatch('PolyFile.PolyFile')
        self.polytecFile.open(filePath)

    def get_velocity(self):
        #TODO: work with try-error
        PointDomains = self.polytecFile.GetPointDomains()
        PointDomainTime = PointDomains.Item('Time')

        ChannelTimeVib = PointDomainTime.Channels.Item('Vib')
        SignalTimeVib = ChannelTimeVib.Signals.Item('Velocity')
        DisplayTimeVib = SignalTimeVib.Displays.Item('Samples')

        DatapointTimeVib = PointDomainTime.Datapoints.Item(1)
        DataTimeVib = np.array(DatapointTimeVib.GetData(DisplayTimeVib, 0))

        return DataTimeVib
    
    def get_voltage(self):
        PointDomains = self.polytecFile.GetPointDomains()
        PointDomainTime = PointDomains.Item('Time')

        ChannelTimeRef1 = PointDomainTime.Channels.Item('Ref1')
        SignalTimeRef1 = ChannelTimeRef1.Signals.Item('Voltage')
        DisplayTimeRef1 = SignalTimeRef1.Displays.Item('Samples')
        DatapointTimeRef1 = PointDomainTime.Datapoints.Item(1)
        DataTimeRef1Voltage = np.array(DatapointTimeRef1.GetData(DisplayTimeRef1, 0))

        return DataTimeRef1Voltage

    def create_fft_plot(self, filename):
        #TODO: work with try-error
        PointDomains = self.polytecFile.GetPointDomains()
        PointDomainFFT = PointDomains.Item('FFT')

        ChannelFFTVib = PointDomainFFT.Channels.Item('Vib')
        SignalFFTVibDisplacement = ChannelFFTVib.Signals.Item('Displacement')
        SignalFFTVibVelocity = ChannelFFTVib.Signals.Item('Velocity')

        FFTVibXmin = SignalFFTVibVelocity.Description.XAxis.Min
        FFTVibXmax = SignalFFTVibVelocity.Description.XAxis.Max
        FFTVibXcount = SignalFFTVibVelocity.Description.XAxis.MaxCount

        DisplayFFTVibVelocity = SignalFFTVibVelocity.Displays('Magnitude')  # .Item('Samples')
        DatapointFFTVibVelocity = PointDomainFFT.datapoints.Item(1)
        DataFFTVibVelocity = np.array(DatapointFFTVibVelocity.GetData(DisplayFFTVibVelocity, 0))

        DataFFTFrequency = np.linspace(FFTVibXmin, FFTVibXmax, FFTVibXcount, endpoint=True, dtype=np.float64)
        myPlotter.fft_plt(DataFFTFrequency, DataFFTVibVelocity, filename)

        return [DataFFTFrequency, DataFFTVibVelocity]
    
    def get_frequency_response(self,):
        #TODO: work with try-error
        PointDomains = self.polytecFile.GetPointDomains()
        PointDomainFFT = PointDomains.Item('FFT')

        ChannelFFTVib = PointDomainFFT.Channels.Item('Vib')
        SignalFFTVibDisplacement = ChannelFFTVib.Signals.Item('Displacement')
        SignalFFTVibVelocity = ChannelFFTVib.Signals.Item('Velocity')

        FFTVibXmin = SignalFFTVibVelocity.Description.XAxis.Min
        FFTVibXmax = SignalFFTVibVelocity.Description.XAxis.Max
        FFTVibXcount = SignalFFTVibVelocity.Description.XAxis.MaxCount

        DisplayFFTVibVelocity = SignalFFTVibVelocity.Displays('Magnitude')  # .Item('Samples')
        DatapointFFTVibVelocity = PointDomainFFT.datapoints.Item(1)
        DataFFTVibVelocity = np.array(DatapointFFTVibVelocity.GetData(DisplayFFTVibVelocity, 0))

        DataFFTFrequency = np.linspace(FFTVibXmin, FFTVibXmax, FFTVibXcount, endpoint=True, dtype=np.float64)

        return [DataFFTFrequency, DataFFTVibVelocity]

    def get_resonance_frequency(self, fMin, fMax):
        frequencyResponse = self.get_frequency_response()
        # from frequencyResponse[0] get the index of the first value that is larger than fMin
        indexMin = np.where(frequencyResponse[0] >= fMin)[0][0]
        indexMax = np.where(frequencyResponse[0] <= fMax)[0][-1]
        #get last value of indexMax
        velocitiesBetweenBoudaries = frequencyResponse[1][indexMin:indexMax]
        frequenciesBetweenBoundaries = frequencyResponse[0][indexMin:indexMax]
        #find the maximum value and the index of frequencyResponse[1] between indexMin and indexMax
        maxIndex = np.argmax(velocitiesBetweenBoudaries)
        #return the value of frequencyResponse[0] at the index of the maximum value
        return frequenciesBetweenBoundaries[maxIndex]
    
    def get_polytec_cc_image(self):
        self.image = self.polytecFile.Infos.VideoBitmap.Image(7, 1920, 1080)[0]
        self.bytes = bytes(self.image)

        self.Stream = io.BytesIO(self.bytes)
        self.Picture = Image.open(self.Stream)
        self.SmallPicture = self.Picture.resize((640, 360), Image.ANTIALIAS)

        self.Array = np.array(self.SmallPicture)
        self.ImageArray = 255 * np.ones((360, 640, 4), dtype=np.uint8)
        self.ImageArray[:, :, 0] = self.Array[:, :, 0]
        self.ImageArray[:, :, 1] = self.Array[:, :, 1]
        self.ImageArray[:, :, 2] = self.Array[:, :, 2]

        self.ScanPoints = np.zeros((0, 2))

        self.Left = self.polytecFile.Infos.MeasPoints.GetVideoRect()[0]
        self.Top = self.polytecFile.Infos.MeasPoints.GetVideoRect()[1]
        self.Right = self.polytecFile.Infos.MeasPoints.GetVideoRect()[2]
        self.Bottom = self.polytecFile.Infos.MeasPoints.GetVideoRect()[3]

        self.ScaleImageX = self.Right - self.Left
        self.ScaleImageY = self.Top - self.Bottom

        for i in range(1, self.polytecFile.Infos.MeasPoints.count+1):

            self.ScanPoints = np.append(self.ScanPoints, np.array([self.polytecFile.Infos.MeasPoints.Item(i).VideoXY()]), axis = 0)

        self.ScanPoints[:, 0] = 640 * (self.ScanPoints[:, 0] - self.Left)/self.ScaleImageX
        self.ScanPoints[:, 1] = 360 - (360 * (self.ScanPoints[:, 1] - self.Bottom) / self.ScaleImageY)

        #self.polytecFile.close()

        self.return_data = {'ImageArray': self.ImageArray, 'ScanPoints': self.ScanPoints}

        return self.return_data
        






            # from frequencyResponse[0] get the index of the first value that is smaller than fMax