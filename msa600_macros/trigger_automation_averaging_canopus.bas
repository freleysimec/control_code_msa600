Dim AnalyzerFileName As String
Dim SettingsFile As String
Dim WorkDir As String
Dim Counter As Integer


Sub Main
	
	Debug.Clear

	WorkDir = "D:\Fre\scans\canopus_scans\"

	' keep waiting for trigger
	Counter = 1

	Dim Nmeas As Integer
	Dim i As Integer
	Nmeas = 1000
	i=0
	j=0
	averaging = 5



	While(i<Nmeas)
		
		' Load settings file
		SettingsFile = "D:\Fre\settings\canopus_noise_scan_4.set"
		Settings.Load(SettingsFile, ptcSettingsAll)

		' Filename
		AnalyzerFileName = DateTime + "_" + CStr(Format(i,"000")) + "_" +".svd"
		Debug.Print AnalyzerFileName

		' Specify filename for area scan
		Acquisition.ScanFileName = WorkDir + AnalyzerFileName

		' Acquisition.Start ptcAcqStartSingle
		' Wait for trigger/pulses, one trigger per point
		' Acquisition.Start ptcAcqStartSingle
		Acquisition.Scan(ptcScanAll)
		'While(j<averaging)
			'Acquisition.Start ptcAcqStartSingle
			'While Acquisition.State <> ptcAcqStateStopped
			'Wait(1)		' wait 0.5 second
			'Wend
			'j=j+1
		'Wend

		' Wait until area scan is finished

		While Acquisition.State <> ptcAcqStateStopped
			Debug.Print "waiting"
			Wait(5)		' wait 5 second
		Wend
		' Scan has finished --> save data

		Acquisition.Document.SaveAs(WorkDir + AnalyzerFileName)

		' Will ignore trigger pulses...
		Wait(5)

		i=i+1
	Wend
	' end of main loop

End Sub


' Return date and time as string
' YYYYMMDD_HHMMSS
Function DateTime

	Dim mDate As String
	Dim mTime As String

	mDate = 	    CStr(Year(Date))
	mDate = mDate + CStr(Format(Month(Date),"00"))
	mDate = mDate + CStr(Format(Day(Date),"00"))

	mTime = 	    CStr(Format(Hour(Time),"00"))
	mTime = mTime + CStr(Format(Minute(Time),"00"))
	mTime = mTime + CStr(Format(Second(Time),"00"))

	DateTime = mDate + "_" + mTime

End Function

