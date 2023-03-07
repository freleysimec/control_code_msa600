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
' The following commands are supported, some of them are tested below
'
' setbeamposition3d,<scanheadindex>,<x_in_m>,<y_in_m>,<z_in_m>
' startsingleshot
' exportascii,<domain>,<channel>,<signal>,<display>,<filename>
'
' The response In Case of an Error Is
' Error,<additional_infos>
'
'#Language "WWB.Net"
' 
Option Explicit

Imports System.Collections.Generic
Imports System.IO
Imports System.Text

Const requestFileName As String = MacroDir() + "\Request.txt"
Const responseFileName As String = MacroDir() + "\Response.txt"

Sub Main
	Debug.Clear

	Dim requests As New List(Of String)


	requests.Add("setbeamposition3d,1,2.38,1.76,-0.03")
	requests.Add("setbeamposition3d,2,2.38,1.76,-0.03")
	requests.Add("setbeamposition3d,3,2.38,1.76,-0.03")
	requests.Add("startsingleshot")
	requests.Add("exportascii,Time,Ref1,Voltage,Samples,D:\Temp\Test.txt")

	Dim responses As List(Of String) = WriteRequestsAndWaitForResponses(requests)
End Sub

' Writes the requests in the specified list to the request file and waits for responses
' in the response file.
Function WriteRequestsAndWaitForResponses(requests As List(Of String)) As List(Of String)
	WriteRequests(requests)
	Dim responses As List(Of String) = ReadResponses()

	Dim index As Long
	For index = 0 To requests.Count - 1
		Debug.Print "Request: ";requests.Item(index)
		Debug.Print "Response: ";responses.Item(index)
	Next

	Return responses
End Function

' Waits until it is possible to open the request file and writes the requests
Sub WriteRequests(requests As List(Of String))
	Dim succeeded As Boolean = False
	While Not succeeded
		Try
			File.WriteAllLines(requestFileName, requests, Encoding.ASCII)
			succeeded = True
		Catch
		End Try
	End While
End Sub

' waits for a response in the response file and reads it
Function ReadResponses() As List(Of String)
	Dim responses As New List(Of String)
	Dim succeeded As Boolean = False
	While Not succeeded
		Try
			responses.AddRange(File.ReadAllLines(responseFileName, Encoding.ASCII))
			succeeded = True
		Catch
		End Try
	End While
	File.Delete(responseFileName)
	Return responses
End Function
