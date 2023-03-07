from win32com.client import Dispatch
import os

def PolytecPVDinfo(self, FullPath):
    self.PolytecFile = Dispatch('PolyFile.PolyFile')

    self.PolytecFile.open(FullPath)
    self.Infos = self.PolytecFile.Infos
    if not self.Infos.AcquisitionInfoModes.ActiveMode and self.Infos.AcquisitionInfoModes.ActiveProperties.HasTimeProperties:
        self.PolytecFile.close()
        return 'Time'
    elif self.Infos.AcquisitionInfoModes.ActiveMode and self.Infos.AcquisitionInfoModes.ActiveProperties.HasFftProperties:
        self.PolytecFile.close()
        return 'FFT'

def PolytecPVDtime(self, input_file):

    self.PointDomains = input_file.GetPointDomains()
    self.PointDomainTime = self.PointDomains.Item('Time')

    self.ChannelTimeVib = self.PointDomainTime.Channels.Item('Vib')
    self.SignalTimeVib = self.ChannelTimeVib.Signals.Item('Velocity')
    self.DisplayTimeVib = self.SignalTimeVib.Displays.Item('Samples')
    self.DatapointTimeVib = self.PointDomainTime.Datapoints.Item(1)

    self.TimeVibXmin = self.SignalTimeVib.Description.XAxis.Min
    self.TimeVibXmax = self.SignalTimeVib.Description.XAxis.Max
    self.TimeVibXcount = self.SignalTimeVib.Description.XAxis.MaxCount
    self.DataTimeVib = np.array(self.DatapointTimeVib.GetData(self.DisplayTimeVib, 0))
    self.DataTimeTime = np.linspace(self.TimeVibXmin, self.TimeVibXmax, self.TimeVibXcount, endpoint=True, dtype=np.float64)

    self.ChannelTimeRef1 = self.PointDomainTime.Channels.Item('Ref1')
    self.SignalTimeRef1 = self.ChannelTimeRef1.Signals.Item('Voltage')
    self.DisplayTimeRef1 = self.SignalTimeRef1.Displays.Item('Samples')
    self.DatapointTimeRef1 = self.PointDomainTime.Datapoints.Item(1)
    self.DataTimeRef1Voltage = np.array(self.DatapointTimeRef1.GetData(self.DisplayTimeRef1, 0))

    return {'Time': {'Time': self.DataTimeTime, 'Velocity': self.DataTimeVib, 'Ref1_voltage':self.DataTimeRef1Voltage}}

def PolytecPVDfft(self, input_file):

    self.PointDomains = input_file.GetPointDomains()
    self.PointDomainFFT = self.PointDomains.Item('FFT')
    self.ChannelFFTVib = self.PointDomainFFT.Channels.Item('Vib')
    self.SignalFFTVibDisplacement = self.ChannelFFTVib.Signals.Item('Displacement')
    self.SignalFFTVibVelocity = self.ChannelFFTVib.Signals.Item('Velocity')


    self.DisplayFFTVibDisplacement = self.SignalFFTVibDisplacement.Displays('Magnitude')  # .Item('Samples')
    self.DatapointFFTVibDisplacement = self.PointDomainFFT.datapoints.Item(1)
    self.DataFFTVibDisplacement = np.array(self.DatapointFFTVibDisplacement.GetData(self.DisplayFFTVibDisplacement, 0))

    self.DisplayFFTVibVelocity = self.SignalFFTVibVelocity.Displays('Magnitude')  # .Item('Samples')
    self.DatapointFFTVibVelocity = self.PointDomainFFT.datapoints.Item(1)
    self.DataFFTVibVelocity = np.array(self.DatapointFFTVibVelocity.GetData(self.DisplayFFTVibVelocity, 0))

    self.FFTVibXmin = self.SignalFFTVibVelocity.Description.XAxis.Min
    self.FFTVibXmax = self.SignalFFTVibVelocity.Description.XAxis.Max
    self.FFTVibXcount = self.SignalFFTVibVelocity.Description.XAxis.MaxCount

    self.DataFFTFrequency = np.linspace(self.FFTVibXmin, self.FFTVibXmax, self.FFTVibXcount, endpoint=True,
                                   dtype=np.float64)

    self.PointDomainTime = self.PointDomains.Item('Time')
    self.ChannelTimeVib = self.PointDomainTime.Channels.Item('Vib')
    self.ChannelTimeRef1 = self.PointDomainTime.Channels.Item('Ref1')

    self.ChannelTimeVib = self.PointDomainTime.Channels.Item('Vib')

    self.SignalTimeVib = self.ChannelTimeVib.Signals.Item('Velocity')
    self.DisplayTimeVib = self.SignalTimeVib.Displays.Item('Samples')
    self.DatapointTimeVib = self.PointDomainTime.Datapoints.Item(1)
    self.DataTimeVib = np.array(self.DatapointTimeVib.GetData(self.DisplayTimeVib, 0))

    self.ChannelTimeRef1 = self.PointDomainTime.Channels.Item('Ref1')
    self.SignalTimeRef1 = self.ChannelTimeRef1.Signals.Item('Voltage')
    self.DisplayTimeRef1 = self.SignalTimeRef1.Displays.Item('Samples')
    self.DatapointTimeRef1 = self.PointDomainTime.Datapoints.Item(1)
    self.DataTimeRef1Voltage = np.array(self.DatapointTimeRef1.GetData(self.DisplayTimeRef1, 0))

    self.SampleResolution = 1/self.Infos.AcquisitionInfoModes.ActiveProperties.FftProperties.SampleFrequency

    return {'FFT': {'Frequency':self.DataFFTFrequency, 'Velocity': self.DataFFTVibVelocity, 'Displacement': self.DataFFTVibDisplacement, 'Ref1_voltage':0}}

def PolytecSVDinfo(self, FullPath):

    self.PolytecFile = Dispatch('PolyFile.PolyFile')

    self.PolytecFile.open(FullPath)
    self.Infos = self.PolytecFile.Infos

    #print('self.Infos', self.Infos)
    #self.PolytecFile.close()

    if not self.Infos.AcquisitionInfoModes.ActiveMode and self.Infos.AcquisitionInfoModes.ActiveProperties.HasTimeProperties:
        #print('Has time')
        self.PolytecFile.close()
        return {'Infos':self.Infos, 'Domain':'Time'}
    elif self.Infos.AcquisitionInfoModes.ActiveMode and self.Infos.AcquisitionInfoModes.ActiveProperties.HasFftProperties:
        #print('Has fft')
        self.PolytecFile.close()
        return {'Infos':self.Infos, 'Domain':'FFT'}

def PolytecSVDfft(self, FullPath, point_index, info):

    self.Info = info

    if self.Info['Domain'] == 'FFT':

        self.point_index = point_index
        self.PolytecFile.open(FullPath)
        self.PolytecInfos = self.PolytecFile.Infos
        self.PointDomains = self.PolytecFile.GetPointDomains()
        self.PointDomain = self.PointDomains.Item('FFT')
        self.ChannelVib = self.PointDomain.Channels.Item('Vib')
        self.ChannelRef1 = self.PointDomain.Channels.Item('Ref1')
        self.ChannelRef2 = self.PointDomain.Channels.Item('Ref2')
        self.ChannelRef3 = self.PointDomain.Channels.Item('Ref3')

        self.SignalVib = self.ChannelVib.Signals.Item('Velocity')
        self.SignalRef1 = self.ChannelRef1.Signals.Item('Voltage')
        self.SignalRef2 = self.ChannelRef2.Signals.Item('Voltage')
        self.SignalRef3 = self.ChannelRef3.Signals.Item('Voltage')

        self.DisplayVib = self.SignalVib.Displays.Item('Magnitude')
        self.DisplayRef1 = self.SignalRef1.Displays.Item('Magnitude')
        self.DisplayRef2 = self.SignalRef2.Displays.Item('Magnitude')
        self.DisplayRef3 = self.SignalRef3.Displays.Item('Magnitude')

        self.DataPoint = self.PointDomain.DataPoints(point_index + 1)

        self.SampleResolution = 1 / self.PolytecInfos.AcquisitionInfoModes.ActiveProperties.FftProperties.SampleFrequency
        self.StartFrequency = self.PolytecInfos.AcquisitionInfoModes.ActiveProperties.FftProperties.StartFrequency
        self.EndFrequency = self.PolytecInfos.AcquisitionInfoModes.ActiveProperties.FftProperties.EndFrequency
        self.Lines = self.PolytecInfos.AcquisitionInfoModes.ActiveProperties.FftProperties.Lines

        self.Frequencies = np.linspace(self.StartFrequency, self.EndFrequency, self.Lines, endpoint=True)

        plt.plot(self.Frequencies, self.DataPoint.GetData(self.DisplayVib, 0), color = 'black')
        plt.plot(self.Frequencies, self.DataPoint.GetData(self.DisplayRef1, 0), color = 'red')
        plt.plot(self.Frequencies, self.DataPoint.GetData(self.DisplayRef2, 0), color = 'green')
        plt.plot(self.Frequencies, self.DataPoint.GetData(self.DisplayRef3, 0), color = 'blue')
        plt.show()


        self.d1 = self.DataPoint.GetData(self.DisplayVib, 0)
        self.d2 = self.DataPoint.GetData(self.DisplayRef1, 0)
        self.d3 = self.DataPoint.GetData(self.DisplayRef2, 0)
        self.d4 = self.DataPoint.GetData(self.DisplayRef3, 0)

        '''
        self.bbbb = irfft(self.d1)
        plt.plot(self.bbbb)
        plt.show()
        '''

        self.output_data = np.array([self.d1, self.d2, self.d3, self.d4])

        self.PolytecFile.close()

        return self.output_data

def PolytecSVDtime(self, FullPath, point_index, info):

    self.Info = info

    if self.Info['Domain'] == 'Time':

        self.point_index = point_index
        self.PolytecFile.open(FullPath)
        self.PolytecInfos = self.PolytecFile.Infos
        self.PointDomains = self.PolytecFile.GetPointDomains()
        self.PointDomain = self.PointDomains.Item('Time')
        self.ChannelVib = self.PointDomain.Channels.Item('Vib')
        self.ChannelRef1 = self.PointDomain.Channels.Item('Ref1')
        self.ChannelRef2 = self.PointDomain.Channels.Item('Ref2')
        self.ChannelRef3 = self.PointDomain.Channels.Item('Ref3')

        self.SignalVib = self.ChannelVib.Signals.Item('Velocity')
        self.SignalRef1 = self.ChannelRef1.Signals.Item('Voltage')
        self.SignalRef2 = self.ChannelRef2.Signals.Item('Voltage')
        self.SignalRef3 = self.ChannelRef3.Signals.Item('Voltage')

        self.DisplayVib = self.SignalVib.Displays.Item('Samples')
        self.DisplayRef1 = self.SignalRef1.Displays.Item('Samples')
        self.DisplayRef2 = self.SignalRef2.Displays.Item('Samples')
        self.DisplayRef3 = self.SignalRef3.Displays.Item('Samples')

        self.DataPoint = self.PointDomain.DataPoints(point_index + 1)

        self.SampleResolution = self.PolytecInfos.AcquisitionInfoModes.ActiveProperties.TimeProperties.SampleResolution
        self.SampleFrequency = self.PolytecInfos.AcquisitionInfoModes.ActiveProperties.TimeProperties.SampleFrequency
        self.Samples = self.PolytecInfos.AcquisitionInfoModes.ActiveProperties.TimeProperties.Samples
        self.SampleTime = self.PolytecInfos.AcquisitionInfoModes.ActiveProperties.TimeProperties.SampleTime

        self.TimeBase = np.linspace(0, self.SampleTime, self.Samples, endpoint=True)

        self.VibSamples = self.DataPoint.GetData(self.DisplayVib, 0)
        self.Ref1Samples = self.DataPoint.GetData(self.DisplayRef1, 0)
        self.Ref2Samples = self.DataPoint.GetData(self.DisplayRef2, 0)
        self.Ref3Samples = self.DataPoint.GetData(self.DisplayRef3, 0)

        '''
        self.bbbb = irfft(self.d1)
        plt.plot(self.bbbb)
        plt.show()
        '''

        #self.output_data = np.array([self.TimeBase, self.VibSamples, self.Ref1Samples, self.Ref2Samples, self.Ref3Samples])
        self.output_data = {'SampleResolution': self.SampleResolution, 'Samples': self.Samples, 'TimeBase': self.TimeBase, 'VibSamples': np.array(self.VibSamples), 'Ref1Samples': 100 * np.array(self.Ref1Samples), 'Ref2Samples': np.array(self.Ref2Samples), 'Ref3Samples': np.array(self.Ref3Samples)}

        self.PolytecFile.close()

        return self.output_data

def PolytecccImage(self, FullPath):
    self.PolytecFile = Dispatch('PolyFile.PolyFile')
    self.PolytecFile.open(FullPath)

    self.Image = self.PolytecFile.Infos.VideoBitmap.Image(7, 1920, 1080)[0]

    self.Bytes = bytes(self.Image)

    self.Stream = io.BytesIO(self.Bytes)
    self.Picture = Image.open(self.Stream)
    self.SmallPicture = self.Picture.resize((640, 360), Image.ANTIALIAS)

    self.Array = np.array(self.SmallPicture)
    self.ImageArray = 255 * np.ones((360, 640, 4), dtype=np.uint8)
    self.ImageArray[:, :, 0] = self.Array[:, :, 0]
    self.ImageArray[:, :, 1] = self.Array[:, :, 1]
    self.ImageArray[:, :, 2] = self.Array[:, :, 2]

    self.ScanPoints = np.zeros((0, 2))

    self.Left = self.PolytecFile.Infos.MeasPoints.GetVideoRect()[0]
    self.Top = self.PolytecFile.Infos.MeasPoints.GetVideoRect()[1]
    self.Right = self.PolytecFile.Infos.MeasPoints.GetVideoRect()[2]
    self.Bottom = self.PolytecFile.Infos.MeasPoints.GetVideoRect()[3]

    self.ScaleImageX = self.Right - self.Left
    self.ScaleImageY = self.Top - self.Bottom

    for i in range(1, self.PolytecFile.Infos.MeasPoints.count+1):

        self.ScanPoints = np.append(self.ScanPoints, np.array([self.PolytecFile.Infos.MeasPoints.Item(i).VideoXY()]), axis = 0)

    self.ScanPoints[:, 0] = 640 * (self.ScanPoints[:, 0] - self.Left)/self.ScaleImageX
    self.ScanPoints[:, 1] = 360 - (360 * (self.ScanPoints[:, 1] - self.Bottom) / self.ScaleImageY)

    self.PolytecFile.close()

    self.return_data = {'ImageArray': self.ImageArray, 'ScanPoints': self.ScanPoints}

    return self.return_data
