from ctypes import wintypes
from pickle import TRUE
import sys
import time
import json
from ctypes import *
import time
import numpy
#https://docs.python.org/3/library/ctypes.html
# OBJdll = cdll.LoadLibrary(r'.\Dll\x64\HTHardDll.dll')

# load dll (64 bit)
# OBJdll = windll.LoadLibrary(r".\Dll\x64\HTHardDll.dll")
# OBJdll = windll.LoadLibrary(r".\Dll\x86\HTHardDll.dll")
OBJdll = windll.LoadLibrary(r".\HTHardDll.dll")

# DEFINTE CLASSES:
# class RelayControl(Structure):
#     bCHEnable = [1] * 4 #Open the channel
#     nCHVoltDIV = [8] * 4 #Set the voltage level
#     nCHCoupling = [1] * 4 #Design coupling mode AC/DC
#     bCHBWLimit = [0] * 4 #Whether to enable 20M filtering
#     nTrigSource = 1 #Trigger source
#     bTrigFilt = 0
#     nALT = 0 #Whether to trigger alternately. Note that alternate triggering is a software function

class RelayControl(Structure):
    _fields_ = [('bCHEnable', c_bool * 4),
    ('nCHVoltDIV', c_ushort * 4),
    ('nCHCoupling', c_ushort * 4),
    ('bCHBWLimit', c_bool * 4),
    ('nTrigSource', c_ushort),
    ('bTrigFilt', c_bool),
    ('nALT', c_ushort)]

# class RelayControl(Structure):
#     _fields_ = [('bCHEnable', POINTER(c_bool)),
#     ('nCHVoltDIV', POINTER(c_ushort)),
#     ('nCHCoupling', POINTER(c_ushort)),
#     ('bCHBWLimit', POINTER(c_bool)),
#     ('nTrigSource', c_ushort),
#     ('bTrigFilt', c_bool),
#     ('nALT', c_ushort)]

class Control(Structure):
    _fields_ = [('nCHSet', c_ushort), #0x0F in hexadecimal notation means all 4 channels are open
    ('nTimeDiv', c_ushort),
    ('nTriggerSource', c_ushort), #Trigger source
    ('nHTriggerPos', c_ushort), #horizontal trigger position
    ('nVTriggerPos', c_ushort), #Vertical trigger position
    ('nTriggerSlope', c_ushort), #Use the rising edge as the trigger method
    ('nBufferLen', c_ushort), # the length of the collected data
    ('nReadDataLen', c_ushort), # the length of the read data
    ('nAlreadyReadLen', c_ushort), # the length that has been read, only used in scan scrolling
    ('nALT', c_ushort)] #Whether to trigger alternately. Note that alternate triggering is a software function

# class Control(Structure):
#     nCHSet = 15 #0x0F in hexadecimal notation means all 4 channels are open
#     nTimeDiv = 11
#     nTriggerSource = 1 #Trigger source
#     nHTriggerPos = 50 #horizontal trigger position
#     nVTriggerPos = 192 #Vertical trigger position
#     nTriggerSlope = 0 #Use the rising edge as the trigger method
#     nBufferLen = 4096 # the length of the collected data
#     nReadDataLen = 4096 # the length of the read data
#     nAlreadyReadLen = 0 # the length that has been read, only used in scan scrolling
#     nALT = 0 #Whether to trigger alternately. Note that alternate triggering is a software function

rcRelayControl = RelayControl()
stControl = Control()

rcRelayControl.bCHEnable = (TRUE, TRUE, TRUE, TRUE) #Open the channel
print(rcRelayControl.bCHEnable)
rcRelayControl.bCHEnable = (c_bool * 4)(*[1,1,1,1])
print(rcRelayControl.bCHEnable)
# rcRelayControl.nCHVoltDIV = (c_ushort * 4)(*[8,8,8,8])
rcRelayControl.nCHVoltDIV = (c_ushort(8), c_ushort(8), c_ushort(8), c_ushort(8))
rcRelayControl.nCHCoupling = (c_ushort * 4)(*[1,1,1,1]) #Design coupling mode AC/DC
rcRelayControl.bCHBWLimit = (c_bool * 4)(*[0,0,0,0]) #Whether to enable 20M filtering
rcRelayControl.nTrigSource = 1 #Trigger source
rcRelayControl.bTrigFilt = 0
rcRelayControl.nALT = 0 #Whether to trigger alternately. Note that alternate triggering is a software function

################################################
#            INITIALIZE VARIABLES
################################################
deviceNum = c_ushort(0)
deviceIndex = c_ushort(0)
leverPos = [192, 160, 96, 64] # [CH1 position, CH2, CH3, CH4]
timeDiv = 11 # Time base index value
YTFormat = 0 # YT Mode


stControl.nCHSet = 15 #0x0F in hexadecimal notation means all 4 channels are open
stControl.nTimeDiv = timeDiv
stControl.nTriggerSource = 1 #Trigger source
stControl.nHTriggerPos = 50 #horizontal trigger position
stControl.nVTriggerPos = leverPos[1] #Vertical trigger position
stControl.nTriggerSlope = 0 #Use the rising edge as the trigger method
stControl.nBufferLen = 4096 # the length of the collected data
stControl.nReadDataLen = 4096 # the length of the read data
stControl.nAlreadyReadLen = 0 # the length that has been read, only used in scan scrolling
stControl.nALT = 0 #Whether to trigger alternately. Note that alternate triggering is a software function


# for i in range(0, 3):
#     rcRelayControl.bCHEnable[i] = 1 #Open the channel
#     rcRelayControl.nCHVoltDIV[i] = 8 #Set the voltage level
#     rcRelayControl.nCHCoupling[i] = 1 #Design coupling mode AC/DC
#     rcRelayControl.bCHBWLimit[i] = 0 #Whether to enable 20M filtering
# rcRelayControl.nTrigSource = stControl.nTriggerSource
# rcRelayControl.bTrigFilt = 0
# rcRelayControl.nALT = stControl.nALT

disLen = 2500 #The screen displays the total number of points
triggerMode = 0 #edge trigger
triggerSlope = 0 #edge-triggered trigger source
triggerSweep = 0 #Auto trigger

readOK = 0
startNew = True
forceTriggerCnt = 0
collect = 1
pAmpLevel = [1024 for i in range(0, 578)] #put 1024 to the hardware, in fact, 1024 means 1.0, that is, no correction

################################################
#           INITIALIZE OSCILLOSCOPE
################################################

print(" --------------------------------------------------------------------------------------------------")

# result = OBJdll.dsoInitHard(deviceIndex)
# print(' = dsoInitHard=',result)

# result = OBJdll.dsoHTADCCHModGain(deviceIndex, 4) #Set the analog amplitude correction
# print('dsoHTADCCHModGain=',result)

# dsoHTSetSampleRate = OBJdll.dsoHTSetSampleRate
# dsoHTSetSampleRate.argtypes = [wintypes.WORD, wintypes.WORD, POINTER(RelayControl), POINTER(Control)]
# dsoHTSetSampleRate.restype = c_ushort
# result = dsoHTSetSampleRate(deviceIndex, YTFormat, rcRelayControl, stControl) #Set the sample rate
# # result = OBJdll.dsoHTSetSampleRate(deviceIndex, YTFormat, rcRelayControl, stControl) #Set the sample rate
# print('dsoHTSetSampleRate=',result)

# dsoHTSetCHAndTrigger = OBJdll.dsoHTSetCHAndTrigger
# dsoHTSetCHAndTrigger.argtypes = [c_ushort, POINTER(RelayControl), c_ushort]
# dsoHTSetCHAndTrigger.restype = c_ushort
# result = dsoHTSetCHAndTrigger(deviceIndex, rcRelayControl, stControl.nTimeDiv) #Set the channel switch and voltage level
# print('dsoHTSetCHAndTrigger=',result)

# result = OBJdll.dsoHTSetRamAndTrigerControl(deviceIndex, stControl.nTimeDiv, stControl.nCHSet, stControl.nTriggerSource, 0) #Set the trigger source
# print('dsoHTSetRamAndTrigerControl=',result)

# # dsoHTSetCHPos = OBJdll.dsoHTSetCHPos
# # dsoHTSetCHPos.argtypes = [c_ushort, c_ushort, c_ushort, c_ushort, c_ushort]
# # dsoHTSetCHPos.restype = c_ushort
# # result = dsoHTSetCHPos(deviceIndex, 6, 128, 0, 4) #Set the vertical position of the channel
# # print('dsoHTSetCHPos=',result)

# # dsoHTSetCHPos = OBJdll.dsoHTSetCHPos
# # dsoHTSetCHPos.argtypes = [c_ushort, c_ushort, c_ushort, c_ushort, c_ushort]
# # dsoHTSetCHPos.restype = c_ushort
# # result = dsoHTSetCHPos(deviceIndex, 8, 128, 0, 4) #Set the vertical position of the channel
# # print('dsoHTSetCHPos=',result)

# # for i in range(0, 3):
# #     dsoHTSetCHPos = OBJdll.dsoHTSetCHPos
# #     dsoHTSetCHPos.argtypes = [c_ushort, c_ushort, c_ushort, c_ushort, c_ushort]
# #     dsoHTSetCHPos.restype = c_ushort
# #     result = dsoHTSetCHPos(deviceIndex, 8, 128, i, 4) #Set the vertical position of the channel
# #     print('dsoHTSetCHPos=',result)

# result = OBJdll.dsoHTSetVTriggerLevel(deviceIndex, leverPos[0], 4) #Set the trigger vertical position to be the same as channel 1
# print('dsoHTSetVTriggerLevel=',result)

# if triggerMode == 0: #EDGE
#     result = OBJdll.dsoHTSetTrigerMode(deviceIndex, triggerMode, stControl.nTriggerSlope, 0) #If it is edge-triggered, call this function
#     print('dsoHTSetTrigerMode=',result)

################################################
#                 COLLECT DATA
################################################

if startNew:
    nStartControl = 0
    nStartControl = nStartControl + (1 if triggerSweep == 0 else 0)
    nStartControl = nStartControl + (0 if YTFormat == 0 else 2)
    nStartControl = nStartControl + (0 if collect == 1 else 4)
    print('nStartControl=',nStartControl)
    result = OBJdll.dsoHTStartCollectData(deviceIndex, nStartControl)
    StartNew = False

# class IN_PARAMS_TRANSFERDATA(Structure):
#     _fields_ = [('pDataBuffer', c_void_p)]


dsoHTGetState = OBJdll.dsoHTGetState
dsoHTGetState.argtypes = [c_ushort]
dsoHTGetState.restype = c_ushort
nState = dsoHTGetState(deviceIndex)
print("state=", nState)
print("(nState & 2)=", (nState & 2))
time.sleep(1)
nState = dsoHTGetState(deviceIndex)
print("state=", nState)
print("(nState & 2)=", (nState & 2))
if ((nState & 2) == 2): # Start reading data at the end of acquisition
    print("READING DATA")
    ################################################
    #                 READ DATA
    ################################################
    # https://stackoverflow.com/questions/37680467/pointer-to-c-int16-array-buffer-in-ctypes
    # https://stackoverflow.com/questions/1363163/pointers-and-arrays-in-python-ctypes
    # https://stackoverflow.com/questions/50819576/python-passing-user-defined-class-by-reference-to-dlls
    CH1ReadData = (c_ushort * 4096)() # the () initializes the array
    CH2ReadData = (c_ushort * 4096)()
    CH3ReadData = (c_ushort * 4096)()
    CH4ReadData = (c_ushort * 4096)()
    # CH1ReadData = create_string_buffer(4096)
    # CH2ReadData = create_string_buffer(4096)
    # CH3ReadData = create_string_buffer(4096)
    # CH4ReadData = create_string_buffer(4096)

    # dsoHTGetRollData = OBJdll.dsoHTGetRollData
    # dsoHTGetRollData.argtypes = [c_ushort, POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort), POINTER(Control)]
    # dsoHTGetRollData.restype = c_ushort
    # result = dsoHTGetRollData(deviceIndex, CH1ReadData, CH2ReadData, CH3ReadData, CH4ReadData, stControl)
    # print('dsoHTGetRollData result=',result)

    # ArrayType = c_int16 * 4096
    # in_data = IN_PARAMS_TRANSFERDATA()
    # data_buffer = ArrayType(1,2,3) # set the first three values
    # in_data.pDataBuffer = c_void_p(addressof(data_buffer)) # or cast(data_buffer, c_void_p)

    # OBJdll.dsoHTGetData(deviceIndex)
    # CH1ReadData[0] = 10
    print(CH1ReadData[0])

    dsoHTGetData = OBJdll.dsoHTGetData
    # dsoHTGetData.argtypes = [c_ushort, POINTER(CH1ReadData), POINTER(CH2ReadData), POINTER(CH3ReadData), POINTER(CH4ReadData), POINTER(Control)]
    # dsoHTGetData.restype = c_ushort
    print("pointer(CH1ReadData)=", pointer(CH1ReadData))
    # print("pointer(CH1ReadData[0]))=", pointer(CH1ReadData[0]))
    print("cast(CH1ReadData, POINTER(c_ushort))=", cast(CH1ReadData, POINTER(c_ushort)))
    print("byref=", byref(CH1ReadData))
    print("addressof=", addressof(CH1ReadData))
    print("c_void_p(addressof(CH1ReadData))=", c_void_p(addressof(CH1ReadData)))
    print("c_void_p(addressof(cast(CH1ReadData, POINTER(c_ushort))))=", c_void_p(addressof(cast(CH1ReadData, POINTER(c_ushort)))))
    # print("in_data=", byref(in_data))
    # NOTE: ffi_prep_cif failed ERROR happens when you don't include argtypes and restype
    dsoHTGetData.argtypes = [c_ushort, POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort), POINTER(Control)]
    # dsoHTGetData.argtypes = [c_ushort, (c_char * 4096), (c_char * 4096), (c_char * 4096), (c_char * 4096), POINTER(Control)]
    # dsoHTGetData.argtypes = [c_ushort, POINTER(c_ushort * 4096), POINTER(c_ushort * 4096), POINTER(c_ushort * 4096), POINTER(c_ushort * 4096), POINTER(Control)]
    dsoHTGetData.restype = c_ushort
    # result = dsoHTGetData(deviceIndex, addressof(CH1ReadData), addressof(CH2ReadData), addressof(CH3ReadData), addressof(CH4ReadData), stControl)
    # result = dsoHTGetData(deviceIndex, pointer(CH1ReadData[0]), pointer(CH2ReadData[0]), pointer(CH3ReadData[0]), pointer(CH4ReadData[0]), stControl)
    # result = dsoHTGetData(deviceIndex, pointer(CH1ReadData), pointer(CH2ReadData), pointer(CH3ReadData), pointer(CH4ReadData), stControl)
    # result = dsoHTGetData(deviceIndex, CH1ReadData[0], CH2ReadData[0], CH3ReadData[0], CH4ReadData[0], stControl)
    result = dsoHTGetData(deviceIndex, CH1ReadData, CH2ReadData, CH3ReadData, CH4ReadData, stControl) # The actual voltage value of the jth point of each channel 1=(CH1ReadData[j]-LeverPos(0 ))*8*Voltage value/255
    # result = dsoHTGetData(deviceIndex, cast(CH1ReadData, POINTER(c_ushort)), cast(CH2ReadData, POINTER(c_ushort)), cast(CH3ReadData, POINTER(c_ushort)), cast(CH4ReadData, POINTER(c_ushort)), stControl) # The actual voltage value of the jth point of each channel 1=(CH1ReadData[j]-LeverPos(0 ))*8*Voltage value/255
    # result = dsoHTGetData(deviceIndex, cast(CH1ReadData[0], POINTER(c_ushort)), cast(CH2ReadData[0], POINTER(c_ushort)), cast(CH3ReadData[0], POINTER(c_ushort)), cast(CH4ReadData[0], POINTER(c_ushort)), stControl)
    print('dsoHTGetData result=',result)
    CH1SrcData = []
    CH2SrcData = []
    CH3SrcData = []
    CH4SrcData = []

    if result == 1:
        for i in range(0, stControl.nReadDataLen - 1):
            CH1SrcData.append(CH1ReadData[i] - (255 - leverPos[0]))
            CH2SrcData.append(CH2ReadData[i] - (255 - leverPos[1]))
            CH3SrcData.append(CH3ReadData[i] - (255 - leverPos[2]))
            CH4SrcData.append(CH4ReadData[i] - (255 - leverPos[3]))
    else:
        print('READ FAILED')
    StartNew = True

    print(CH1SrcData)
else:
    print("DEVICE NOT READY FOR READ")
    StartNew = False

# print("COMPLETED!!!!!!")