'#Reference {07B59BE6-A0F1-4B9C-ACEB-F68719C36488}#2.0#0#C:\Windows\Microsoft.Net\assembly\GAC_MSIL\Polytec.IO.VibController\v4.0_2.0.0.0__e9bf5e9b998cc19f\Polytec.IO.VibController.dll#Polytec IO VibController Type Library#Polytec_IO_VibController
'#Reference {B24D8715-8901-4293-9938-AC3FBFBC9E8A}#1.0#0#C:\Program Files\Common Files\ActiveXperts\AxSerial64.dll#ActiveXperts Serial Port Component 3.2 Type Library#AxSerial
'#Reference {450A9894-D9C9-11D1-9966-0000F840FC5E}#1.0#0#C:\PROGRA~1\COMMON~1\Polytec\COM\ACTIVE~1.OCX#ActiveDSO ActiveX Control module#ACTIVEDSOLib
'#uses "SwitchToAcquisitionMode.bas"

	Dim Commport As New ComPort			'RS232 port
	Dim Co As Integer
	Dim RXbuff As String
	Dim RXX() As String

Sub Main

	Debug.Clear
	If Not SwitchToAcquisitionMode() Then
		MsgBox("Switch to acquisition mode failed.", vbOkOnly)
		End
	End If

	Set Commport = New ComPort
	Commport.ClearRX
	Commport.ClearTX

	Commport.LogFile = "SerialPort.log"
    'Debug.Print "Log file used: " + Commport.LogFile
    Commport.Device = "COM1"
	Commport.BaudRate =  9600
	Commport.ComTimeout = 10000
	Commport.Open()

	While 1
	
		RXbuff = Commport.ReadString()
		Debug.Print("Waiting here" + RXbuff)

		If Len(RXbuff)>3 Then
			RXX = Split(RXbuff, "	")

			If RXX(0) = "SetScanFileName" Then
				Acquisition.ScanFileName = RXX(1)
				Commport.ClearRX
				Commport.ClearTX
				Wait(2)
				Commport.WriteString(RXbuff + " - Done\r")
				Wait(2)

			ElseIf RXX(0) = "ScanAll" Then
				Debug.Print("AcqFileName: " + Acquisition.ScanFileName)

				Acquisition.Scan ptcScanAll
				Commport.ClearRX
				Commport.ClearTX
				Wait(0.1)
				Commport.WriteString(RXbuff + " - armed\r")
				Wait(0.1)

				While Acquisition.State <> ptcAcqStateStopped
					Wait(1)
				Wend
				Commport.ClearRX
				Commport.ClearTX
				Wait(1)
				Commport.WriteString(RXbuff + " - Done\r")
				Wait(1)


			ElseIf RXX(0) = "SinglePointContinuousStart" Then
				Acquisition.Start ptcAcqStartContinuous
				Wait(1)

			ElseIf RXX(0) = "SinglePointContinuousStop" Then
				Acquisition.Stop

			ElseIf RXX(0) = "UserAcquisitionSettingsFileName" Then
				Debug.Print("aaa	" + RXX(0) + "	" + RXX(1))
				Wait(2)
				Commport.ClearRX
				Commport.ClearTX
				Wait(2)
				Settings.Load RXX(1), ptcSettingsAcquisition
				Commport.WriteString(RXbuff + " - Done\r")
				Wait(2)

			ElseIf RXX(0) = "UserAllSettingsFileName" Then
				Debug.Print("aaa	" + RXX(0) + "	" + RXX(1))
				Wait(2)
				Commport.ClearRX
				Commport.ClearTX
				Wait(2)
				Settings.Load RXX(1), ptcSettingsAll
				Commport.WriteString(RXbuff + " - Done\r")
				Wait(2)


			ElseIf RXX(0) = "UserScanPointsSettingsFileName" Then
				Debug.Print("aaa	" + RXX(0) + "	" + RXX(1))
				Wait(2)
				Commport.ClearRX
				Commport.ClearTX
				Wait(2)
				Settings.Load RXX(1), ptcSettingsAPS
				Commport.WriteString(RXbuff + " - Done\r")
				Wait(2)

			ElseIf RXX(0) = "CaptureImage" Then
				Debug.Print("bbb	" + RXX(0) + "	" + RXX(1))
				Wait(1)
				Commport.ClearRX
				Commport.ClearTX
				Wait(1)

				Commport.WriteString(RXbuff + " - Done\r")
				Wait(1)

			ElseIf RXX(0) = "*IDN?" Then
				Debug.Print("bbb	" + RXX(0))
				Wait(1)
				Commport.ClearRX
				Commport.ClearTX
				Wait(1)
				Commport.WriteString("My name is MSV400. Polytec MSV-400. - Done\r")
				Wait(1)
			Else
				Debug.Print("bbb	" + RXX(0))
				Wait(1)
				Commport.ClearRX
				Commport.ClearTX
				Wait(1)
				Commport.WriteString("My name is MSV400. Polytec MSV-400. - Done\r")
				Wait(1)



			End If


			'Debug.Print RXX(1)
		End If

		Wait 1
	Wend

End Sub
