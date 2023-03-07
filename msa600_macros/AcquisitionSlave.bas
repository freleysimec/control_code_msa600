'#Reference {53D4F9AB-9B83-40F5-BE0C-E155C88B67A7}#1.0#0#D:\Dev\Main\bin\Debug64\PolyHardlock.dll#Polytec PolyHardlock Type Library
' Polytec Macro: AcquisitionMaster.bas
' ------------------------------------
'
' This macro allows to remote control a PSV acquisition system.
'
' 1. Copy the macros AcquisitionMaster.bas and AcquisitionSlave.bas
'    to a network share that is accessibale by the master (PSV presentation) and the slave (PSV aquisition)
' 3. Start AcquisitionSlave.bas in acquistion mode of the PSV software
'    on the PSV slave system.
' 4. Start AcquisitionMaster.bas in presentation mode of the PSV software
'    on the PSV master system.
'
' The following commands are supported
'
' setbeamposition3d,<scanheadindex>,<x_in_m>,<y_in_m>,<z_in_m>
' startsingleshot
' exportascii,<domain>,<channel>,<signal>,<display>,<filename>
'
' The response In Case of an Error Is
' Error,<additional_infos>
'
'#Language "WWB.Net"

Option Explicit

Imports System.Collections.Generic
Imports System.Globalization
Imports System.IO
Imports System.Text

Const requestFileName As String = MacroDir() + "\requests.txt"
Const responseFileName As String = MacroDir() + "\response.txt"
Const waitTimeAfterDeleteFileBeforeScan As Double = 0.1 ' seconds

Dim applicationMessageText As String

' Main function executes endless loop of reading requests, executing and writing responses
Sub Main
	



	Debug.Print "starting"
	Debug.Clear

	'If Not SwitchToAcquisitionMode() Then
		'MsgBox("Switch to acquisition mode failed.", vbOkOnly)
		'End
	'End If

	TryDeleteFile(requestFileName)
	TryDeleteFile(responseFileName)

	Do
		Dim requests As List(Of String) = ReadRequests()
		Wait 1
		Dim responses As List(Of String) = ExecuteRequests(requests)
		Call WriteResponses(responses)
	Loop
End Sub

' Tries to delete the specified file. Ignores any errors (e.g. file does not exist)
Sub TryDeleteFile(fileName As String)
	Debug.Print "try deleting"
	Try
		File.Delete(fileName)
	Catch
	End Try
End Sub

' Executes the specified requests
Function ExecuteRequests(requests As List(Of String)) As List(Of String)
	Debug.Print "execute requests"
	Dim responses As New List(Of String)
	For Each request As String In requests
		Debug.Print "Request: ";request
		Dim response As String = TryExecuteRequest(request)
		Debug.Print "Response: ";response
		responses.Add(response)
	Next
	Return responses
End Function

' Tries to execute the specified request. If an error occurs the error message is
' returned instead of the regular response of the command.
Function TryExecuteRequest(request As String) As String
	Dim response As New StringBuilder()
	Dim exc As System.Exception
	Try
		response.Append(ExecuteRequest(request))
	Catch ex As System.Exception
		exc = ex
	End Try

	If (Not exc Is Nothing) Or (Not String.IsNullOrWhiteSpace(applicationMessageText)) Then
		If (response.Length > 0) Then response.Append(",")
		response.Append(FormatErrorMessage(exc))
		applicationMessageText = String.Empty
	End If

	Return response.ToString()
End Function

' Executes a request and returns the response.
Function ExecuteRequest(request As String) As String
	Dim strCommand As String = Extract(request, 0)
	Select Case UCase(strCommand)
		Case "SETBEAMPOSITION3D"
			ExecuteRequest = SetBeamPosition3D(CLng(Extract(request, 1)), CDblInvariant(Extract(request, 2)), CDblInvariant(Extract(request, 3)), CDblInvariant(Extract(request, 4)))
		Case "START_SINGLE_SHOT"
			ExecuteRequest = StartSingleShot()
		Case "SCAN_AND_SAVE"
			ExecuteRequest = ScanAndSave(Extract(request, 1))
		Case "CHANGE_SETTINGS"
			ExecuteRequest = loadSettings(Extract(request, 1))
		Case "EXPORTASCII"
			ExecuteRequest = ExportAscii(Extract(request, 1), Extract(request, 2), Extract(request, 3), Extract(request, 4), Extract(request, 5))
		Case "SET_FILE_NAME"
			ExecuteRequest = SetFileName(Extract(request, 1))
		Case "SET_ACTUATION_FREQUENCY"
			ExecuteRequest = SetActuationFrequency(Extract(request, 1), Extract(request, 2))
		Case Else
			ExecuteRequest = "error,unknown request: " + request
	End Select
End Function

' Converts string with decimal point to a double independent of the locale
Function CDblInvariant(value As String) As Double
	Return Double.Parse(value, CultureInfo.InvariantCulture)
End Function

' Formats an error message from the error object.
Function FormatErrorMessage(ex As System.Exception) As String
	Dim errorMessage As String = "error"
	If (Not ex Is Nothing) Then
		errorMessage = errorMessage + ",1," + ex.Message
	End If
	If (Len(applicationMessageText) > 0) Then
		errorMessage = errorMessage + "," + FormatApplicationMessage(applicationMessageText)
	End If
	Return errorMessage
End Function

' Format the application message such that it does not contain any new lines or commas, because that would conflict
' with our response format
Function FormatApplicationMessage(applicationMessage As String) As String
	applicationMessage = Replace(applicationMessage, vbCrLf, " ")
	applicationMessage = Replace(applicationMessage, vbCr, " ")
	applicationMessage = Replace(applicationMessage, vbLf, " ")
	applicationMessage = Replace(applicationMessage, ",", ";")
	Return applicationMessage
End Function

' Ignore application messages that are expected. Returns true if the message should be ignored.
Function IgnoreApplicationMessage(message As String) As Boolean
	message = FormatApplicationMessage(message)
	If (message = "The definition of Measurement Locations is not complete. Do you still want to proceed?") Then
		Return True
	ElseIf (message = "Die Definition der Tabelle der Messstellen ist nicht vollst�ndig angegeben. M�chten Sie trotzdem fortfahren?") Then
		Return True
	ElseIf (message = "The acquisition sample frequency is less than the waveform frequency.") Then
		Return True
	ElseIf (message = "Die Abtastfrequenz ist kleiner als die Frequenz der Signalform.") Then
		Return True
	End If
	Return False
End Function

' Event handler for handling message boxes that would be displayed in PSV if no macro were running.
Public Sub ApplicationMessageOccurred(ByVal messageStyle As PTCMessageStyle, ByVal Text As String, ByRef answer As PTCMessageAnswer)
	If (Not IgnoreApplicationMessage(Text)) Then
		applicationMessageText = Text
	End If
End Sub

' Extracts the n'th token from the specified request string
Function Extract(request As String, index As Integer) As String
	Return Split(request, ",")(index)
End Function

' Sets the scanner position of the scanning head with the specified index to the position calculated from
' the 3D alignment with the specified 3D coordinate.
Function SetBeamPosition3D(scanHeadIndex As Integer, x As Double, y As Double, z As Double) As String
	Dim oInfosAcq As InfosAcq = Acquisition.Infos
	Dim oAlign3D As Alignment3D = oInfosAcq.Alignments.Alignments3D.Item(scanHeadIndex)
	Dim scannerX As Double
	Dim scannerY As Double
	Dim distance As Double

	oAlign3D.Coord3DToScanner(x, y, z, scannerX, scannerY, distance)

	Dim oScanHeadDevice As ScanHeadDevice = oInfosAcq.ScanHeadDevicesInfo.ScanHeadDevices(scanHeadIndex)
	oScanHeadDevice.ScanHeadControl.ScannerControl.SetBeamPosition(scannerX, scannerY)
	Return String.Format(CultureInfo.InvariantCulture, "beamposition3d,{0},{1},{2},{3}", scanHeadIndex, x, y, z)
End Function

' Starts a single shot measurement at the current scanner position and waits until it has finished.
Function StartSingleShot() As String
	Acquisition.Start(PTCAcqStartMode.ptcAcqStartSingle)
	While (Acquisition.State <> PTCAcqState.ptcAcqStateStopped)
		Wait 0.1
	End While
	Return "singleshotfinished"
End Function

' Configures the display of the current analyzer window for the specified domain, channel, signal and display and exports
' the displayed data as ASCII to the specified filename.
Function ExportAscii(domainName As String, channelName As String, signalName As String, displayName As String, fileName As String) As String
	Debug.Print "ExportAscii"
	If (Application.ActiveWindow Is Nothing Or Application.ActiveWindow.Type <> PTCWindowType.ptcWindowTypeAnalyzer) Then
		Application.ActiveDocument.NewWindow()
	End If
	Dim oAnalyzerWindow As AnalyzerWindow = Application.ActiveWindow

	Dim oDisplaySettings As DisplaySettings = oAnalyzerWindow.AnalyzerView.Settings.DisplaySettings

	Select Case UCase(domainName)
	Case "TIME", "ZEIT"
		oDisplaySettings.Domain = PTCDomainType.ptcDomainTime
	Case "FFT"
		oDisplaySettings.Domain = PTCDomainType.ptcDomainSpectrum
	End Select

	oDisplaySettings.Channel = channelName
	oDisplaySettings.Signal = signalName

	oDisplaySettings.Display = oAnalyzerWindow.AnalyzerView.Display.Signal.Displays.Item(displayName).Type
	oAnalyzerWindow.AnalyzerView.Export(fileName, PTCFileFormat.ptcFileFormatText)

	Return "exportascii," + domainName + "," + channelName + "," +  signalName + "," + displayName + "," + fileName
End Function

' Function ExportSvd(domainName As String, channelName As String, signalName As String, displayName As String, fileName As String) As String
	

' 	Return "exportascii," + domainName + "," + channelName + "," +  signalName + "," + displayName + "," + fileName
' End Function

' Waits until it is possible to open the response file and then writes the responses.
Sub WriteResponses(responses As List(Of String))
	Dim succeeded As Boolean = False
	While Not succeeded
		Try
			File.WriteAllLines(responseFileName, responses, Encoding.ASCII)
			succeeded = True
		Catch
		End Try
	End While
End Sub

' Waits for the request file and reads all requests in it. Then deletes the file.
Function ReadRequests() As List(Of String)
	Debug.Print "readRequests"
	Dim requests As New List(Of String)
	Dim succeeded As Boolean = False
	While Not succeeded
		Try
			requests.AddRange(File.ReadAllLines(requestFileName, Encoding.ASCII))
			succeeded = True
		Catch
		End Try
	End While
	File.Delete(requestFileName)
	Return requests
End Function

Function SetFileName(fileName As String) As String
	Debug.Print "SetFileName"
	Acquisition.ScanFileName = fileName
	Return "filename: " + fileName
End Function

Function loadSettings(settingsFileName As String) As String
	Debug.Print "loadSettings"
	Settings.Load(settingsFileName, PTCSettings.ptcSettingsAll)

	Return "Settingsfile changed"
End Function

Function ScanAndSave(fileNameAndPath As String) As String
	Debug.Print "ScanAndSave"
	Acquisition.ScanFileName = fileNameAndPath
	Acquisition.Scan(PTCScanMode.ptcScanAll)
	While Acquisition.State <> PTCAcqState.ptcAcqStateStopped
			Wait(0.5)		' wait 5 second
	End While
	'Acquisition.Document.SaveAs("joske")
	Return "scanned and saved"
End Function

Function SetActuationFrequency(settingsFile As String, frequencyAmount As Double) As String
	'Debug.Print "SetActuationFrequency"
'
	'Dim oFile As New PolyFile
	'oFile.Open(settingsFile)
	'Dim oAcqInfos As AcquisitionInfoModes = oFile.Infos.Type(PTCInfoType.ptcInfoAcquisition)
	'Dim oAcqProps As AcquisitionPropertiesContainer = oAcqInfos.ActiveProperties
	'Dim oGeneratorsAcqProps As GeneratorsAcqPropertiesContainer = oAcqProps(PTCAcqPropertiesType.ptcAcqPropertiesTypeGenerators)
	'Dim oGeneratorAcqProps As GeneratorAcqProperties = oGeneratorsAcqProps(1)
	'Dim oWaveform As Waveform = oGeneratorAcqProps.Waveform
	'Dim oSine As WaveformSine = oWaveform
	'oFile.Close()
'
	''oFile.SaveAsEx(PTCSaveAs.ptcSaveAsTypeInfos, fileName)
'
'
	'Dim bFile As New PolyFile
	'Dim bAcqInfos As AcquisitionInfoModes = oAcqInfos
	'Dim myFrequency As Double = 123.0
	'Dim mySine As WaveformSine
	'Debug.Print "1"
	'mySine.Frequency = 123.0
'
'
	'Debug.Print "myFrequency"
	'Debug.Print myFrequency
	'Debug.Print "mySine"
	'Debug.Print mySine.Frequency
'
	'Dim myWaveform As Waveform = mySine
'
	'Dim myGeneratorAcqProps As GeneratorAcqProperties
	'myGeneratorAcqProps.Waveform = myWaveform
	'Dim myGeneratorsAcqProps As GeneratorsAcqPropertiesContainer
	'myGeneratorsAcqProps(1) = myGeneratorAcqProps
	'Dim myAcqProps As AcquisitionPropertiesContainer
	'myAcqProps(PTCAcqPropertiesType.ptcAcqPropertiesTypeGenerators) = myGeneratorsAcqProps
	'Dim myAcqInfos As AcquisitionInfoModes
'
'
	'bFile.Infos.Add(myAcqInfos.ActiveMode)
'
'
'
	'Dim fileName As String = "C:\Users\MMICRO\Desktop\control_software\communication_directory\joske.set"
	'bFile.SaveAsEx(PTCSaveAs.ptcSaveAsTypeInfos, fileName)
	'bFile.Close()





	Return "not implemented"


End Function
