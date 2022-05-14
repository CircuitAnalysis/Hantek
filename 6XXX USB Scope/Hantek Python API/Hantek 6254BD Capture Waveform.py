from ctypes import wintypes
from pickle import TRUE
import sys
import time
import json
from ctypes import *
import time
import numpy
import matplotlib.pyplot as plt
#https://docs.python.org/3/library/ctypes.html
# load dll (cdll or windll)
OBJdll = windll.LoadLibrary(r".\Dll\x64\HTHardDll.dll") # (64 bit)
# OBJdll = windll.LoadLibrary(r".\Dll\x86\HTHardDll.dll") # (32 bit)

class RELAYCONTROL(Structure):
    _fields_ = [('bCHEnable', wintypes.BOOL * 4),
    ('nCHVoltDIV', wintypes.WORD * 4),
    ('nCHCoupling', wintypes.WORD * 4),
    ('bCHBWLimit', wintypes.BOOL * 4),
    ('nTrigSource', wintypes.WORD),
    ('bTrigFilt', wintypes.BOOL),
    ('nALT', wintypes.WORD)]

class DATACONTROL(Structure):
    _fields_ = [('nCHSet', wintypes.WORD), #0x0F in hexadecimal notation means all 4 channels are open
    ('nTimeDIV', wintypes.WORD),
    ('nTriggerSource', wintypes.WORD), #Trigger source
    ('nHTriggerPos', wintypes.WORD), #horizontal trigger position
    ('nVTriggerPos', wintypes.WORD), #Vertical trigger position
    ('nTriggerSlope', wintypes.WORD), #Use the rising edge as the trigger method
    ('nBufferLen', wintypes.ULONG), # the length of the collected data
    ('nReadDataLen', wintypes.ULONG), # the length of the read data
    ('nAlreadyReadLen', wintypes.ULONG), # the length that has been read, only used in scan scrolling
    ('nALT', wintypes.WORD), #Whether to trigger alternately. Note that alternate triggering is a software function
    ('nETSOpen', wintypes.WORD),
    ('nDriverCode', wintypes.WORD), # drive number
    ('nLastAddress', wintypes.ULONG), # record the last read end address of scan mode
    ('nFPGAVersion', wintypes.WORD)] #FPGA version number
    #('nAddressOffset', wintypes.WORD) #Trigger jitter plus offset

################################################
#            INITIALIZE VARIABLES
################################################

#SIGNAL GENERATOR
FREQUENCY = 17000 # Hz
AMPLITUDE = 1000 # mV-peak
OFFSET = 0 # mV
WAVE_TYPE = 0 #0=sine, 1=ramp, 2=square, 4=DC, 8=noise
WAVE_MODE = 0 #0=continuous wave, 1=single wave

#OSCILLOSCOPE:
PROBE_MULTIPLIER = 1 # 1 or 10 x probe
ADC_CHANNEL_MODE = 4 #1, 2 or 4
ENABLED_CHANNELS = [1, 1, 1, 1]
CHANNEL_COUPLING = 0 # DC=0, AC=1
CHANS_MASK = 0x0F # 0x0F in hexadecimal notation means all 4 channels are open

TRIGGER_CHANNEL = 0 #CH1=0, CH2=1, CH3=2, CH4=3
TRIGGER_SLOPE = 0 # rising=0
TRIGGER_MODE = 0 # edge=0
TRIGGER_SWEEP = 0 # Auto trigger
TRIGGER_COUPLE = 1 # DC=0, AC=1
TRIGGER_V = 0 # Trigger Voltage (vertical)

#0=2nS, 1=5nS, 2=10nS, 3=20nS, 4=50nS, 5=100nS, 6=200nS, 7=500nS, 8=1uS, 9=2uS, 10=5uS, 11=10uS, 12=20uS, 13=50uS, 14=100uS, 15=200uS, 16=500uS 
#17=1mS, 18=2mS, 19=5mS, 20=10mS, 21=20mS, 22=50mS, 23=100mS, 24=200mS, 25=500mS, 26=1S, 27=2S, 28=5S, 29=10S, 30=20S
#31=50S, 32=100S, 33=200S, 34=500S, 35=1000S
TIME_PER_DIVISION = 11
TIME_MULT = [2E-9, 5E-9, 1E-8, 2E-8, 5E-8, 1E-7, 2E-7, 5E-7, 1E-6, 2E-6, 5E-6, 1E-5, 2E-5, 5E-5, 1E-4, 2E-4, 5E-4, 1E-3, 2E-3, 5E-3, 1E-2, 2E-2, 5E-2, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
SAMPLING_RATE_SINGLE = [1E9, 1E9, 1E9, 1E9, 1E9, 1E9, 1E9, 500E6, 250E6, 125E6, 50E6, 25E6, 12.5E6, 5E6, 2.5E6, 1.25E6, 500E3, 250E3, 125E3, 50E3, 25E3, 12.5E3, 5E3, 2.5E3, 1.25E3, 500, 250, 125, 50, 25, 12.5, 5, 2.5, 1.25, 0.5, 0.25]
SAMPLING_RATE_DUAL =   [500E6, 500E6, 500E6, 500E6, 500E6, 500E6, 500E6, 500E6, 250E6, 125E6, 50E6, 25E6, 12.5E6, 5E6, 2.5E6, 1.25E6, 500E3, 250E3, 125E3, 50E3, 25E3, 12.5E3, 5E3, 2.5E3, 1.25E3, 500, 250, 125, 50, 25, 12.5, 5, 2.5, 1.25, 0.5, 0.25]
SAMPLING_RATE_QUAD =   [250E6, 250E6, 250E6, 250E6, 250E6, 250E6, 250E6, 250E6, 250E6, 125E6, 50E6, 25E6, 12.5E6, 5E6, 2.5E6, 1.25E6, 500E3, 250E3, 125E3, 50E3, 25E3, 12.5E3, 5E3, 2.5E3, 1.25E3, 500, 250, 125, 50, 25, 12.5, 5, 2.5, 1.25, 0.5, 0.25]

#0=2mV, 1=5mV, 2=10mV, 3=20mV, 4=50mV, 5=100mV, 6=200mV, 7=500mV, 8=1V, 9=2V, 10=5V, 11=10V (w/ x1 probe)
VOLTS_PER_DIVISION = 7
VOLT_MULT = [0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]
VOLT_DIVISIONS = 8
VOLT_RESOLUTION = 256 #8 bit ADC

CH_ZERO_POS = [128, 128, 128, 128] # vertical zero position 0-255 [CH1, CH2, CH3, CH4]

YTFormat = 0 # YT Mode
collect = 1
nStartControl = 0
nStartControl = nStartControl + (1 if TRIGGER_SWEEP == 0 else 0)
nStartControl = nStartControl + (0 if YTFormat == 0 else 2)
nStartControl = nStartControl + (0 if collect == 1 else 4)

rcRelayControl = RELAYCONTROL()
stDataControl = DATACONTROL()

rcRelayControl.bCHEnable = (wintypes.BOOL * 4)(*ENABLED_CHANNELS)
rcRelayControl.nCHVoltDIV = (wintypes.WORD * 4)(VOLTS_PER_DIVISION,VOLTS_PER_DIVISION,VOLTS_PER_DIVISION,VOLTS_PER_DIVISION)
rcRelayControl.nCHCoupling = (wintypes.WORD * 4)(CHANNEL_COUPLING,CHANNEL_COUPLING,CHANNEL_COUPLING,CHANNEL_COUPLING) #Design coupling mode DC=0, AC=1
rcRelayControl.bCHBWLimit = (wintypes.BOOL * 4)(0,0,0,0) #Whether to enable 20M filtering
rcRelayControl.nTrigSource = TRIGGER_CHANNEL #Trigger source
rcRelayControl.bTrigFilt = 0 #Whether to enable 20M filtering
rcRelayControl.nALT = 0 #Whether to trigger alternately. Note that alternate triggering is a software function

stDataControl.nCHSet = CHANS_MASK #0x0F (15) means all 4 channels are open
stDataControl.nTimeDIV = TIME_PER_DIVISION # Time base index value
stDataControl.nTriggerSource = TRIGGER_CHANNEL #Trigger source
stDataControl.nHTriggerPos = 50 #horizontal trigger position
stDataControl.nVTriggerPos = TRIGGER_V #Vertical trigger position
stDataControl.nTriggerSlope = TRIGGER_SLOPE #Use the rising edge as the trigger method
stDataControl.nBufferLen = 4096 # the length of the collected data
stDataControl.nReadDataLen = 4096 # the length of the read data
stDataControl.nAlreadyReadLen = 0 # the length that has been read, only used in scan scrolling
stDataControl.nALT = 0 #Whether to trigger alternately. Note that alternate triggering is a software function

stDataControl.nCHSet = 15 #0x0F (15) means all 4 channels are open
stDataControl.nTimeDIV = 10 # Time base index value
stDataControl.nTriggerSource = 2 #Trigger source
stDataControl.nHTriggerPos = 0 #horizontal trigger position
stDataControl.nVTriggerPos = 10 #Vertical trigger position
stDataControl.nTriggerSlope = 1 #Use the rising edge as the trigger method
stDataControl.nBufferLen = 4096 # the length of the collected data
stDataControl.nReadDataLen = 4096 # the length of the read data
stDataControl.nAlreadyReadLen = 0 # the length that has been read, only used in scan scrolling
stDataControl.nALT = 0 #Whether to trigger alternately. Note that alternate triggering is a software function

################################################
#           FIND AND INITIALIZE DEVICE
################################################

print(" --------------------------------------------------------------------------------------------------")

#Find the currently connected device and get its index number
deviceArray = (wintypes.WORD * 32)()
deviceIndex = wintypes.WORD(99)
dsoHTSearchDevice = OBJdll.dsoHTSearchDevice
dsoHTSearchDevice.argtypes = [POINTER(wintypes.WORD)]
dsoHTSearchDevice.restype = wintypes.WORD
result = dsoHTSearchDevice(deviceArray)
if result == 0:
    raise Exception("Device not found!")

for i in range(32):
    # print(i,'=',deviceArray[i])
    if deviceArray[i]:
        deviceIndex = i
        break
print("Found Device Index: ", deviceIndex)

dsoInitHard = OBJdll.dsoInitHard
dsoInitHard.argtypes = [wintypes.WORD]
dsoInitHard.restype = wintypes.WORD
result = dsoInitHard(deviceIndex)
print('dsoInitHard=',result)

################################################
#     INITIALIZE FUNCTION GENERATOR (DDS)
################################################

ddsSetCmd = OBJdll.ddsSetCmd
ddsSetCmd.argtypes = [wintypes.WORD, wintypes.USHORT]
ddsSetCmd.restype = wintypes.ULONG
result = ddsSetCmd(deviceIndex, WAVE_MODE)
print('ddsSetCmd=',result)

ddsSDKSetWaveType = OBJdll.ddsSDKSetWaveType
ddsSDKSetWaveType.argtypes = [wintypes.WORD, wintypes.WORD]
ddsSDKSetWaveType.restype = wintypes.WORD
result = ddsSDKSetWaveType(deviceIndex, WAVE_TYPE)
print('ddsSDKSetWaveType=',result)

ddsSDKSetFre = OBJdll.ddsSDKSetFre
ddsSDKSetFre.argtypes = [wintypes.WORD, wintypes.FLOAT]
ddsSDKSetFre.restype = wintypes.FLOAT
result = ddsSDKSetFre(deviceIndex, FREQUENCY)
print('ddsSDKSetFre=',result)

ddsSDKSetAmp = OBJdll.ddsSDKSetAmp
ddsSDKSetAmp.argtypes = [wintypes.WORD, wintypes.WORD]
ddsSDKSetAmp.restype = wintypes.WORD
result = ddsSDKSetAmp(deviceIndex, AMPLITUDE)
print('ddsSDKSetAmp=',result)

ddsSDKSetOffset = OBJdll.ddsSDKSetOffset
ddsSDKSetOffset.argtypes = [wintypes.WORD, wintypes.SHORT]
ddsSDKSetOffset.restype = wintypes.SHORT
result = ddsSDKSetOffset(deviceIndex, OFFSET)
print('ddsSDKSetOffset=',result)

ddsSetOnOff = OBJdll.ddsSetOnOff
ddsSetOnOff.argtypes = [wintypes.WORD, wintypes.SHORT]
ddsSetOnOff.restype = wintypes.ULONG
result = ddsSetOnOff(deviceIndex, 1)
print('ddsSetOnOff=',result)

print("Completed DDS Configuration")

################################################
#         INITIALIZE OSCILLOSCOPE (DSO)
################################################

dsoHTADCCHModGain = OBJdll.dsoHTADCCHModGain
dsoHTADCCHModGain.argtypes = [wintypes.WORD, wintypes.WORD]
dsoHTADCCHModGain.restype = wintypes.WORD
result = dsoHTADCCHModGain(deviceIndex, 4) #Set the analog amplitude correction
print('dsoHTADCCHModGain=',result)

dsoHTSetSampleRate = OBJdll.dsoHTSetSampleRate
dsoHTSetSampleRate.argtypes = [wintypes.WORD, wintypes.WORD, POINTER(RELAYCONTROL), POINTER(DATACONTROL)]
dsoHTSetSampleRate.restype = wintypes.WORD
result = dsoHTSetSampleRate(deviceIndex, YTFormat, rcRelayControl, stDataControl) #Set the sample rate
print('dsoHTSetSampleRate=',result)

dsoHTSetCHAndTrigger = OBJdll.dsoHTSetCHAndTrigger
dsoHTSetCHAndTrigger.argtypes = [wintypes.WORD, POINTER(RELAYCONTROL), wintypes.WORD]
dsoHTSetCHAndTrigger.restype = wintypes.WORD
result = dsoHTSetCHAndTrigger(deviceIndex, rcRelayControl, stDataControl.nTimeDIV) #Set the channel switch and voltage level
print('dsoHTSetCHAndTrigger=',result)

dsoHTSetRamAndTrigerControl = OBJdll.dsoHTSetRamAndTrigerControl
dsoHTSetRamAndTrigerControl.argtypes = [wintypes.WORD, wintypes.WORD, wintypes.WORD, wintypes.WORD, wintypes.WORD]
dsoHTSetRamAndTrigerControl.restype = wintypes.WORD
result = dsoHTSetRamAndTrigerControl(deviceIndex, stDataControl.nTimeDIV, stDataControl.nCHSet, stDataControl.nTriggerSource, 0) #Set the trigger source
print('dsoHTSetRamAndTrigerControl=',result)

for i in range(4):
    dsoHTSetCHPos = OBJdll.dsoHTSetCHPos
    dsoHTSetCHPos.argtypes = [wintypes.WORD, wintypes.WORD, wintypes.WORD, wintypes.WORD, wintypes.WORD]
    dsoHTSetCHPos.restype = wintypes.WORD
    result = dsoHTSetCHPos(deviceIndex, rcRelayControl.nCHVoltDIV[i], CH_ZERO_POS[i], i, ADC_CHANNEL_MODE) #Set the vertical position of the channel
    print('rcRelayControl.nCHVoltDIV[i]=', rcRelayControl.nCHVoltDIV[i])
    print('dsoHTSetCHPos=',result, ' CH', i+1)

dsoHTSetVTriggerLevel = OBJdll.dsoHTSetVTriggerLevel
dsoHTSetVTriggerLevel.argtypes = [wintypes.WORD, wintypes.WORD, wintypes.WORD]
dsoHTSetVTriggerLevel.restype = wintypes.WORD
result = dsoHTSetVTriggerLevel(deviceIndex, stDataControl.nVTriggerPos, 4) #Set the trigger vertical position to be the same as channel 1
print('dsoHTSetVTriggerLevel=',result)

dsoHTSetTrigerMode = OBJdll.dsoHTSetTrigerMode
dsoHTSetTrigerMode.argtypes = [wintypes.WORD, wintypes.WORD, wintypes.WORD, wintypes.WORD]
dsoHTSetTrigerMode.restype = wintypes.WORD
result = dsoHTSetTrigerMode(deviceIndex, TRIGGER_MODE, stDataControl.nTriggerSlope, 0)
print('dsoHTSetTrigerMode=',result)

################################################
#                 COLLECT DATA
################################################
dsoHTStartCollectData = OBJdll.dsoHTStartCollectData
dsoHTStartCollectData.argtypes = [wintypes.WORD, wintypes.WORD]
dsoHTStartCollectData.restype = wintypes.WORD
result = dsoHTStartCollectData(deviceIndex, nStartControl)
print('dsoHTStartCollectData=',result)

print("Waiting for measurement to complete")
dsoHTGetState = OBJdll.dsoHTGetState
dsoHTGetState.argtypes = [wintypes.WORD]
dsoHTGetState.restype = wintypes.WORD
while (dsoHTGetState(deviceIndex) & 2) == 0:
    time.sleep(0.001) #wait 1 mS
print("Data is ready to read, READING DATA")

################################################
#                 READ DATA
################################################

# https://stackoverflow.com/questions/37680467/pointer-to-c-int16-array-buffer-in-ctypes
# https://stackoverflow.com/questions/1363163/pointers-and-arrays-in-python-ctypes
# https://stackoverflow.com/questions/50819576/python-passing-user-defined-class-by-reference-to-dlls
CH1ReadData = (wintypes.WORD * 4096)() # the () initializes the array
CH2ReadData = (wintypes.WORD * 4096)()
CH3ReadData = (wintypes.WORD * 4096)()
CH4ReadData = (wintypes.WORD * 4096)()

# NOTE: ffi_prep_cif failed ERROR happens when you don't include argtypes and restype
dsoHTGetData = OBJdll.dsoHTGetData
dsoHTGetData.argtypes = [wintypes.WORD, POINTER(wintypes.WORD), POINTER(wintypes.WORD), POINTER(wintypes.WORD), POINTER(wintypes.WORD), POINTER(DATACONTROL)]
dsoHTGetData.restype = wintypes.WORD
result = dsoHTGetData(deviceIndex, CH1ReadData, CH2ReadData, CH3ReadData, CH4ReadData, stDataControl)
print('dsoHTGetData result=',result)

timeData = []
CH1SrcData = []
CH2SrcData = []
CH3SrcData = []
CH4SrcData = []
if result == 1:
    for i in range(stDataControl.nReadDataLen):
        # Calculate Time Points
        if(ADC_CHANNEL_MODE == 1):
            curSampleRate = SAMPLING_RATE_SINGLE[TIME_PER_DIVISION]
        elif(ADC_CHANNEL_MODE == 2):
            curSampleRate = SAMPLING_RATE_DUAL[TIME_PER_DIVISION]
        elif(ADC_CHANNEL_MODE == 4):
            curSampleRate = SAMPLING_RATE_QUAD[TIME_PER_DIVISION]
        else:
            print('ADC_CHANNEL_MODE can only be 1, 2 or 4, aborting.')
        timeData.append(i / curSampleRate)
        CH1SrcData.append((CH1ReadData[i] - (255 - CH_ZERO_POS[0])) * PROBE_MULTIPLIER * VOLT_MULT[VOLTS_PER_DIVISION] * VOLT_DIVISIONS / 256)
        CH2SrcData.append((CH2ReadData[i] - (255 - CH_ZERO_POS[1])) * PROBE_MULTIPLIER * VOLT_MULT[VOLTS_PER_DIVISION] * VOLT_DIVISIONS / 256)
        CH3SrcData.append((CH3ReadData[i] - (255 - CH_ZERO_POS[2])) * PROBE_MULTIPLIER * VOLT_MULT[VOLTS_PER_DIVISION] * VOLT_DIVISIONS / 256)
        CH4SrcData.append((CH4ReadData[i] - (255 - CH_ZERO_POS[3])) * PROBE_MULTIPLIER * VOLT_MULT[VOLTS_PER_DIVISION] * VOLT_DIVISIONS / 256)
else:
    print('READ FAILED')

# Use MatPlotLib to plot the waveforms 
fig, ax = plt.subplots()

ax.set(xlabel='time (S)', ylabel='voltage (V)', title='WAVEFORM')

ax.plot(timeData, CH1SrcData, "-g", label="CH1")
ax.plot(timeData, CH2SrcData, "-b", label="CH2")
ax.plot(timeData, CH3SrcData, "-r", label="CH3")
ax.plot(timeData, CH4SrcData, "-y", label="CH4")

ax.grid()
plt.legend(loc="upper left")
plt.xlim([0, timeData[4095]]) #Note, in the official software I believe the windows shows 2500 sample (time) points
verticalHeight = VOLT_MULT[VOLTS_PER_DIVISION] * VOLT_DIVISIONS / 2
plt.ylim([-verticalHeight, verticalHeight])
plt.show()

print("COMPLETED!")