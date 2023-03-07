from win32com.client import Dispatch
import numpy as np
import io as io

def polytec_PVD_info(FullPath):
    polytecFile = Dispatch('PolyFile.PolyFile')
    polytecFile.open(FullPath)

    Infos = polytecFile.Infos
    if not Infos.AcquisitionInfoModes.ActiveMode and Infos.AcquisitionInfoModes.ActiveProperties.HasTimeProperties:
        polytecFile.close()
        print('Time')
        return 'Time'
    elif Infos.AcquisitionInfoModes.ActiveMode and Infos.AcquisitionInfoModes.ActiveProperties.HasFftProperties:
        polytecFile.close()
        print('FFT')
        return 'FFT'

def polytec_PVD_time(FullPath):

    polytecFile = Dispatch('PolyFile.PolyFile')
    polytecFile.open(FullPath)

    PointDomains = polytecFile.GetPointDomains()
    PointDomainTime = PointDomains.Item('Time')

    ChannelTimeVib = PointDomainTime.Channels.Item('Vib')
    SignalTimeVib = ChannelTimeVib.Signals.Item('Velocity')
    DisplayTimeVib = SignalTimeVib.Displays.Item('Samples')
    DatapointTimeVib = PointDomainTime.Datapoints.Item(1)

    TimeVibXmin = SignalTimeVib.Description.XAxis.Min
    TimeVibXmax = SignalTimeVib.Description.XAxis.Max
    TimeVibXcount = SignalTimeVib.Description.XAxis.MaxCount
    DataTimeVib = np.array(DatapointTimeVib.GetData(DisplayTimeVib, 0))
    DataTimeTime = np.linspace(TimeVibXmin, TimeVibXmax, TimeVibXcount, endpoint=True, dtype=np.float64)

    ChannelTimeRef1 = PointDomainTime.Channels.Item('Ref1')
    SignalTimeRef1 = ChannelTimeRef1.Signals.Item('Voltage')
    DisplayTimeRef1 = SignalTimeRef1.Displays.Item('Samples')
    DatapointTimeRef1 = PointDomainTime.Datapoints.Item(1)
    DataTimeRef1Voltage = np.array(DatapointTimeRef1.GetData(DisplayTimeRef1, 0))

    return {'Time': {'Time': DataTimeTime, 'Velocity': DataTimeVib, 'Ref1_voltage':DataTimeRef1Voltage}}

def polytec_cc_image( FullPath):
    PolytecFile = Dispatch('PolyFile.PolyFile')
    PolytecFile.open(FullPath)

    Image = PolytecFile.Infos.VideoBitmap.Image(7, 1920, 1080)[0]

    Bytes = bytes(Image)

    Stream = io.BytesIO(Bytes)
    Picture = Image.open(Stream)
    SmallPicture = Picture.resize((640, 360), Image.ANTIALIAS)

    Array = np.array(SmallPicture)
    ImageArray = 255 * np.ones((360, 640, 4), dtype=np.uint8)
    ImageArray[:, :, 0] = Array[:, :, 0]
    ImageArray[:, :, 1] = Array[:, :, 1]
    ImageArray[:, :, 2] = Array[:, :, 2]

    ScanPoints = np.zeros((0, 2))

    Left = PolytecFile.Infos.MeasPoints.GetVideoRect()[0]
    Top = PolytecFile.Infos.MeasPoints.GetVideoRect()[1]
    Right = PolytecFile.Infos.MeasPoints.GetVideoRect()[2]
    Bottom = PolytecFile.Infos.MeasPoints.GetVideoRect()[3]

    ScaleImageX = Right - Left
    ScaleImageY = Top - Bottom

    for i in range(1, PolytecFile.Infos.MeasPoints.count+1):

        ScanPoints = np.append(ScanPoints, np.array([PolytecFile.Infos.MeasPoints.Item(i).VideoXY()]), axis = 0)

    ScanPoints[:, 0] = 640 * (ScanPoints[:, 0] - Left)/ScaleImageX
    ScanPoints[:, 1] = 360 - (360 * (ScanPoints[:, 1] - Bottom) / ScaleImageY)

    PolytecFile.close()

    return_data = {'ImageArray': ImageArray, 'ScanPoints': ScanPoints}

    return return_data