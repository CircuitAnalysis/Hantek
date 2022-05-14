Imports System



Module Program
    'Sub Main(args As String())
    '    Console.WriteLine("Hello World!")

    '    Dim i As Long

    '    Dim result As Integer
    '    Dim CH1ReadData(4096) As Integer
    '    Dim CH2ReadData(4096) As Integer
    '    Dim CH3ReadData(4096) As Integer
    '    Dim CH4ReadData(4096) As Integer
    '    result = dsoHTGetData(DeviceIndex, CH1ReadData(0), CH2ReadData(0), CH3ReadData(0), CH4ReadData(0), stControl)
    '    If result = 1 Then
    '        For i = 0 To stControl.nReadDataLen - 1
    '            'CH1SrcData(i) = CH1ReadData(i) - (255 - LeverPos(0))
    '            'CH2SrcData(i) = CH2ReadData(i) - (255 - LeverPos(1))
    '            'CH3SrcData(i) = CH3ReadData(i) - (255 - LeverPos(2))
    '            'CH4SrcData(i) = CH4ReadData(i) - (255 - LeverPos(3))
    '        Next i
    '    End If
    'End Sub

    'USB
    'dsoHTSearchDevice(short* pDevInfo);
    Public Declare Function dsoHTSearchDevice Lib "HTHardDll.dll" (DevInfo As Integer) As Integer
    'dsoHTSetSampleRate(WORD nDeviceIndex,WORD *pAmpLevel,WORD nYTFormat,PRELAYCONTROL pRelayControl,PCONTROLDATA pControl)
    Public Declare Function dsoHTSetSampleRate Lib "HTHardDll.dll" (ByVal nDeviceIndex As Integer, ByVal nYTFormat As Integer, pRelayControl As RelayControl, pSTControl As CONTROLDATA) As Integer
    'dsoHTSetCHAndTrigger(WORD nDeviceIndex,PRELAYCONTROL pRelayControl,WORD nDriverCode,PCONTROLDATA pControl)
    Public Declare Function dsoHTSetCHAndTrigger Lib "HTHardDll.dll" (ByVal nDeviceIndex As Integer, rcRelayControl As RelayControl, ByVal nTimeDiv As Integer) As Integer
    'dsoHTSetHTriggerLength(WORD nDeviceIndex,ULONG nBufferLen,WORD HTriggerPos,WORD nTimeDIV,WORD nCHMod);
    Public Declare Function dsoHTSetHTriggerLength Lib "HTHardDll.dll" (ByVal nDeviceIndex As Integer, ByVal nBufferLen As Long, ByVal HTriggerPos As Integer, ByVal nTimeDiv As Integer, ByVal nYTFormat As Integer) As Integer
    'dsoHTGetState(WORD nDeviceIndex);
    Public Declare Function dsoHTGetState Lib "HTHardDll.dll" (ByVal nDeviceIndex As Integer) As Integer
    'dsoHTSetCHAndTriggerVB(WORD nDeviceIndex,WORD* pCHEnable,WORD* pCHVoltDIV,WORD* pCHCoupling,WORD* pCHBWLimit,WORD nTriggerSource,WORD nTriggerFilt,WORD nALT,WORD nDriverCode);
    Public Declare Function dsoHTSetCHAndTriggerVB Lib "HTHardDll.dll" (ByVal nDeviceIndex As Integer, ByRef CHEnable As Integer, ByRef CHVoltDIV As Integer, ByRef CHCoupling As Integer, ByRef CHBWLimit As Integer, ByVal nTriggerSource As Integer, ByVal nTriggerFilt As Integer, ByVal nALT As Integer) As Integer
    'dsoHTGetData(WORD nDeviceIndex,WORD* pCH1Data,WORD* pCH2Data,WORD* pCH3Data,WORD* pCH4Data,PCONTROLDATA pControl/*,ULONG* p1,ULONG* p2,ULONG* p3*/)


    Public Declare Function dsoHTGetData Lib "HTHardDll.dll" (ByVal nDeviceInder As Integer, CH1Data As Integer, CH2Data As Integer, CH3Data As Integer, CH4Data As Integer, pSTControl As CONTROLDATA) As Integer
    'dsoHTStartCollectData(WORD nDeviceIndex,WORD nStartControl)
    Public Declare Function dsoHTStartCollectData Lib "HTHardDll.dll" (ByVal nDeviceIndex As Integer, ByVal startcontrol As Long) As Integer
    'dsoHTSetTrigerMode(WORD m_nDeviceIndex,WORD nTriggerMode,WORD nTriggerSlop,WORD nTriggerCouple);
    Public Declare Function dsoHTSetTrigerMode Lib "HTHardDll.dll" (ByVal nDeviceIndex As Integer, ByVal TriggerMode As Integer, ByVal Slop As Integer, ByVal TriCouple As Integer) As Integer
    'dsoHTSetVTriggerLevel(WORD nDeviceIndex,WORD* pLevel,WORD nPos,WORD nSensitivity);
    Public Declare Function dsoHTSetVTriggerLevel Lib "HTHardDll.dll" (ByVal nDeviceIndex As Integer, ByVal nPos As Integer, ByVal chmod As Integer) As Integer
    'dsoHTSetCHPos(WORD nDeviceIndex,WORD* pLevel,WORD nVoltDIV,WORD nPos,WORD nCH,WORD nCHMode)
    Public Declare Function dsoHTSetCHPos Lib "HTHardDll.dll" (ByVal nDeviceInder As Integer, ByVal CHVoltDIV As Integer, ByVal CHPos As Integer, ByVal CH As Integer, ByVal chmod As Integer) As Integer

    'dsoInitADCOnce(WORD DeviceIndex)
    Public Declare Function dsoInitHard Lib "HTHardDll.dll" (ByVal nDeviceInder As Integer) As Integer
    'dsoHTADCCHModGain(WORD DeviceIndex,WORD nCHMod);
    Public Declare Function dsoHTADCCHModGain Lib "HTHardDll.dll" (ByVal nDeviceInder As Integer, ByVal nCHMod As Integer) As Integer
    'dsoHTSetRamAndTrigerControl(WORD DeviceIndex,WORD nTimeDiv,WORD nCHset,WORD nTrigerSource,WORD nPeak)
    Public Declare Function dsoHTSetRamAndTrigerControl Lib "HTHardDll.dll" (ByVal DeviceIndex As Integer, ByVal TimeDIV As Integer, ByVal CHSet As Integer, ByVal nTriggerSource As Integer, ByVal isPeak As Integer) As Integer

    'Draw
    Public Declare Function HTDrawGrid Lib "HTDisplayDll.dll" (ByVal hDC As Long, ByVal nLeft As Long, ByVal nTop As Long, ByVal nRight As Long, ByVal nBottom As Long, ByVal nHoriGridNum As Long, ByVal nVertGridNum As Long, ByVal nBright As Long, ByVal IsGrid As Long) As Long
    Public Declare Function HTDrawWaveInYTVB Lib "HTDisplayDll.dll" (ByVal hDC As Long, ByVal Left As Long, ByVal Top As Long, ByVal Right As Long, ByVal Bottom As Long, ByVal R As Integer, ByVal G As Integer, ByVal B As Integer, ByVal nDisTye As Integer, ByRef pData As Integer, ByVal nLen As Long, ByVal nDisLen As Long, ByVal CenterData As Long, ByVal nDisLeverPos As Integer, ByVal Horizontal As Double, ByVal Vertical As Double, ByVal YTFormat As Integer, ByVal AlreadLen As Long) As Long

    Structure RelayControl 'SDK_HTHardDll_CHS.pdf
        Public bCHEnable(3) As Long
        Public nCHVoltDIV(3) As Integer
        Public nCHCoupling(3) As Long
        Public bCHBWLimit(3) As Integer
        Public nTrigSource As Integer
        Public bTrigFilt As Long
        Public nALT As Integer
    End Structure

    Structure CONTROLDATA 'SDK_HTSoftDll_CHS.pdf
        Public nCHSet As Integer
        Public nTimeDiv As Integer
        Public nTriggerSource As Integer
        Public nHTriggerPos As Integer
        Public nVTriggerPos As Integer
        Public nTriggerSlope As Integer
        Public nBufferLen As Long
        Public nReadDataLen As Long
        Public nAlreadyReadLen As Long
        Public nALT As Integer
        Public nETSOpen As Integer
        Public nDriverCode As Integer
        Public nLastAddress As Long
    End Structure

    Structure COLORREF
        Public R As Integer
        Public G As Integer
        Public B As Integer
    End Structure

    Structure RECT
        Public Left As Integer
        Public Top As Integer
        Public Right As Integer
        Public Bottom As Integer
    End Structure
    '''''''''''''

    Public DeviceNum As Long
    Public DeviceIndex As Integer
    Public CH1SrcData(4096) As Integer
    Public CH2SrcData(4096) As Integer
    Public CH3SrcData(4096) As Integer
    Public CH4SrcData(4096) As Integer
    Public CH1Color As COLORREF
    Public CH2Color As COLORREF
    Public CH3Color As COLORREF
    Public CH4Color As COLORREF
    Public CalLevel(578) As Integer
    Public TimeDIV As Integer
    Public YTFormat As Integer
    Public stControl As CONTROLDATA
    Public rcRelayControl As RelayControl
    Public TriggerMode As Integer
    Public TriggerSweep As Integer
    Public TriggerSlope As Integer
    Public LeverPos(3) As Integer
    Public ReadOK As Long
    Public StartNew As Boolean
    Public DisLen As Long
    Public Collect As Integer
    Public pAmpLevel(578) As Integer

    Sub Main()
        Dim DevInfo(63) As Integer
        Dim result As Long
        Dim ip(4) As Integer
        InitializeVariables() 'Initialize variables
        DeviceNum = dsoHTSearchDevice(DevInfo(0))
        If DeviceNum = 0 Then
            MsgBox("DSO not found!")
            End
        End If
        InitHard() 'Initialize hardware
        MainForm.Visible = True
        MainForm.GetDataLoop.Enabled = True
    End Sub

    Public Sub InitializeVariables()
        Dim i As Long
        i = 0
        DeviceNum = 0
        DeviceIndex = 0 'device index value
        LeverPos(0) = 192 'CH1 position
        LeverPos(1) = 160 'CH2 position
        LeverPos(2) = 96 'CH3 position
        LeverPos(3) = 64 'CH4 position
        TimeDIV = 11 'Time base index value
        YTFormat = 0 'YT mode
        stControl.nCHSet = 15 '0x0F in hexadecimal notation means all 4 channels are open
        stControl.nTimeDiv = TimeDIV
        stControl.nTriggerSource = 1 'Trigger source
        stControl.nHTriggerPos = 50 'horizontal trigger position
        stControl.nVTriggerPos = LeverPos(1) 'Vertical trigger position
        stControl.nTriggerSlope = 0 'Use the rising edge as the trigger method
        stControl.nBufferLen = 4096 ' the length of the collected data
        stControl.nReadDataLen = 4096 ' the length of the read data
        stControl.nAlreadyReadLen = 0 ' the length that has been read, only used in scan scrolling
        DisLen = 2500 'The screen displays the total number of points
        stControl.nALT = 0 'Whether to trigger alternately. Note that alternate triggering is a software function
        For i = 0 To 3
            rcRelayControl.bCHEnable(i) = 1 'Open the channel
            rcRelayControl.nCHVoltDIV(i) = 8 'Set the voltage level
            rcRelayControl.nCHCoupling(i) = 1 'Design coupling mode AC/DC
            rcRelayControl.bCHBWLimit(i) = 0 'Whether to enable 20M filtering
        Next i
        rcRelayControl.nTrigSource = stControl.nTriggerSource
        rcRelayControl.bTrigFilt = 0
        rcRelayControl.nALT = stControl.nALT
        TriggerMode = 0 'edge trigger
        TriggerSlope = 0 'edge-triggered trigger source
        TriggerSweep = 0 'Auto trigger
        ReadOK = 0
        StartNew = True
        'ForceTriggerCnt = 0
        Collect = 1
        For i = 0 To 578
            pAmpLevel(i) = 1024 'put 1024 to the hardware, in fact, 1024 means 1.0, that is, no correction
        Next i

    End Sub


    Public Sub InitHard()
        Dim result As Long
        DeviceIndex = 0
        Dim i As Integer
        Dim nVolt As Integer
        result = dsoInitHard(DeviceIndex) ' the second function called after hardware connection
        result = dsoHTADCCHModGain(DeviceIndex, 4) 'Set the analog amplitude correction
        result = dsoHTSetSampleRate(DeviceIndex, YTFormat, rcRelayControl, stControl) 'Set the sample rate
        result = dsoHTSetCHAndTrigger(DeviceIndex, rcRelayControl, stControl.nTimeDiv) 'Set the channel switch and voltage level
        result = dsoHTSetRamAndTrigerControl(DeviceIndex, (stControl.nTimeDiv), (stControl.nCHSet), (stControl.nTriggerSource), 0) 'Set the trigger source
        For i = 0 To 3
            result = dsoHTSetCHPos(DeviceIndex, rcRelayControl.nCHVoltDIV(i), LeverPos(i), i, 4) 'Set the vertical position of the channel
        Next i

        result = dsoHTSetVTriggerLevel(DeviceIndex, LeverPos(0), 4) 'Set the trigger vertical position to be the same as channel 1
        If TriggerMode = 0 Then 'EDGE
            result = dsoHTSetTriggerMode(DeviceIndex, TriggerMode, stControl.nTriggerSlope, 0) 'If it is edge-triggered, call this function
        End If
    End Sub


    Public Sub CollectData()
        Dim nState As Long
        Dim result As Long
        If (StartNew) Then
            Dim nStartControl As Integer
            nStartControl = 0
            nStartControl = nStartControl + IIf(TriggerSweep = 0, 1, 0)
            nStartControl = nStartControl + IIf(YTFormat = 0, 0, 2)
            nStartControl = nStartControl + IIf(Collect = 1, 0, 4)
            result = dsoHTStartCollectData(DeviceIndex, nStartControl)
            StartNew = False
        End If
        nState = dsoHTGetState(DeviceIndex)
        If (nState And 2) = 2 Then ' Start reading data at the end of acquisition
            ReadData()
            StartNew = True
        Else

            StartNew = False

        End If
    End Sub

    Public Sub ReadData()
        Dim i As Long

        Dim result As Integer
        Dim CH1ReadData(4096) As Integer
        Dim CH2ReadData(4096) As Integer
        Dim CH3ReadData(4096) As Integer
        Dim CH4ReadData(4096) As Integer
        result = dsoHTGetData(DeviceIndex, CH1ReadData(0), CH2ReadData(0), CH3ReadData(0), CH4ReadData(0), stControl) 'The actual voltage value of the jth point of each channel 1=(CH1ReadData[j]-LeverPos(0 ))*8*Voltage value/255
        If result = 1 Then
            For i = 0 To stControl.nReadDataLen - 1
                CH1SrcData(i) = CH1ReadData(i) - (255 - LeverPos(0))
                CH2SrcData(i) = CH2ReadData(i) - (255 - LeverPos(1))
                CH3SrcData(i) = CH3ReadData(i) - (255 - LeverPos(2))
                CH4SrcData(i) = CH4ReadData(i) - (255 - LeverPos(3))
            Next i
        End If
    End Sub
End Module
