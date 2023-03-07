from win32com.client import Dispatch
import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
import os

class Svd:
    def __init__(self, resultsDirectory, filename):
        self.filePath = os.path.join(resultsDirectory, filename + ".svd")
        self.polytecFile = Dispatch('PolyFile.PolyFile')
        self.polytecFile.open(self.filePath)
    
    def get_svd_info(self):
        self.Infos = self.polytecFile.Infos

        if not self.Infos.AcquisitionInfoModes.ActiveMode and self.Infos.AcquisitionInfoModes.ActiveProperties.HasTimeProperties:
            # print('Has time')
            #self.polytecFile.close()
            return {'Infos':self.Infos, 'Domain':'Time'}
        elif self.Infos.AcquisitionInfoModes.ActiveMode and self.Infos.AcquisitionInfoModes.ActiveProperties.HasFftProperties:
            # print('Has fft')
            #self.polytecFile.close()
            return {'Infos':self.Infos, 'Domain':'FFT'}
    
    # gets array with frequency and velocity for each point: points go from 1 to amount of points
    def get_frequency_response(self, point = 1):

        info = self.get_svd_info()

        if info['Domain'] == 'FFT':
            polytecInfos = self.polytecFile.Infos
            pointDomains = self.polytecFile.GetPointDomains()
            pointDomain = pointDomains.Item('FFT')
            channelVib = pointDomain.Channels.Item('Vib')
            signalVib = channelVib.Signals.Item('Displacement') #TODO take displacement
            displayVib = signalVib.Displays.Item('Magnitude')
            dataPoint = pointDomain.dataPoints(point)

            #sampleResolution = 1 / polytecInfos.AcquisitionInfoModes.ActiveProperties.FftProperties.SampleFrequency
            startFrequency = polytecInfos.AcquisitionInfoModes.ActiveProperties.FftProperties.StartFrequency
            endFrequency = polytecInfos.AcquisitionInfoModes.ActiveProperties.FftProperties.EndFrequency
            lines = polytecInfos.AcquisitionInfoModes.ActiveProperties.FftProperties.Lines
            FFTVibXmin = signalVib.Description.XAxis.Min
            FFTVibXmax = signalVib.Description.XAxis.Max
            FFTVibXcount = signalVib.Description.XAxis.MaxCount
            frequencies = np.linspace(startFrequency, endFrequency, FFTVibXcount, endpoint=True)
            displacements = dataPoint.GetData(displayVib, 0)

            #plt.plot(d1, color = 'black')
            # plt.plot(frequencies, displacements, color = 'black')
            # plt.show()
            outputData = np.array([frequencies, displacements])

            return outputData

        if info['Domain'] == 'Time':
            pass
            #print('Time')

    def plot_frequency_response(self, frequencyResponse):
        plt.plot(frequencyResponse[0], frequencyResponse[1], color = 'black')
        plt.show()

    def get_image(self):
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

    def get_resonance_frequency(self, point, fMin, fMax):
        frequencyResponse = self.get_frequency_response(point=point)
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

    def get_amplitude_at_frequency(self, point, frequency):
        frequencyResponse = self.get_frequency_response(point=point)
        index = np.where(frequencyResponse[0] == frequency)[0][0]
        return frequencyResponse[1][index]

    def get_voltage(self, point):
        info = self.get_svd_info()

        if info['Domain'] == 'FFT':
            polytecInfos = info['Infos']
            pointDomains = self.polytecFile.GetPointDomains()
            pointDomain = pointDomains.Item('FFT')
            channelRef2 = pointDomain.Channels.Item('Ref2')
            signalRef2 = channelRef2.Signals.Item('Voltage') #TODO take displacement
            displayRef2 = signalRef2.Displays.Item('Magnitude')
            dataPoint = pointDomain.dataPoints(point)

            #sampleResolution = 1 / polytecInfos.AcquisitionInfoModes.ActiveProperties.FftProperties.SampleFrequency
            startFrequency = polytecInfos.AcquisitionInfoModes.ActiveProperties.FftProperties.StartFrequency
            endFrequency = polytecInfos.AcquisitionInfoModes.ActiveProperties.FftProperties.EndFrequency
            lines = polytecInfos.AcquisitionInfoModes.ActiveProperties.FftProperties.Lines
            FFTVibXmin = signalRef2.Description.XAxis.Min
            FFTVibXmax = signalRef2.Description.XAxis.Max
            FFTRef2Xcount = signalRef2.Description.XAxis.MaxCount
            frequencies = np.linspace(startFrequency, endFrequency, FFTRef2Xcount, endpoint=True)
            voltages = dataPoint.GetData(displayRef2, 0)

            #plt.plot(d1, color = 'black')
            # plt.plot(frequencies, displacements, color = 'black')
            # plt.show()
            outputData = np.array([frequencies, voltages])

            return outputData

        if info['Domain'] == 'Time':
            print('time domain')
            