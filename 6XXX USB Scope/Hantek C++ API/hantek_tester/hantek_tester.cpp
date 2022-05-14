// hantek_tester.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <Windows.h>
#include "DefMacro.h"
#include "HTSoftDll.h"
#include "HTHardDll.h"

#include <iostream>
#include <fstream>
#include <cstdlib>
#include <iomanip>
#include <string>

//constexpr size_t FIRST_ENABLED_CHAN = 0;
// Note: more needs to be done to support less than 4 channels enabled
constexpr size_t ADC_CHANNEL_MODE = 4; //1, 2 or 4
constexpr int ENABLED_CHANNELS[4] = {1, 1, 1, 1};
constexpr size_t CHANS_MASK = 0x0F; // 0x0F in hexadecimal notation means all 4 channels are open
constexpr int TRIGGER_CHANNEL = 0; //CH1=0, CH2=1, CH3=2, CH4=3
constexpr int TRIGGER_SLOPE = RISE;
constexpr int TRIGGER_MODE = EDGE;
constexpr int TRIGGER_COUPLE = AC;
constexpr int CHANNEL_COUPLING = AC;
//0=2nS, 1=5nS, 2=10nS, 3=20nS, 4=50nS, 5=100nS, 6=200nS, 7=500nS, 8=1uS, 9=2uS, 10=5uS, 11=10uS, 12=20uS, 13=50uS, 14=100uS, 15=200uS, 16=500uS 
//17=1mS, 18=2mS, 19=5mS, 20=10mS, 21=20mS, 22=50mS, 23=100mS, 24=200mS, 25=500mS, 26=1S, 27=2S, 28=5S, 29=10S, 30=20S
//31=50S, 32=100S, 33=200S, 34=500S, 35=1000S
constexpr int TIME_PER_DIVISION = 11; //20 uS
constexpr double TIME_MULT[36] = { 2E-9, 5E-9, 1E-8, 2E-8, 5E-8, 1E-7, 2E-7, 5E-7, 1E-6, 2E-6, 5E-6, 1E-5, 2E-5, 5E-5, 1E-4, 2E-4, 5E-4, 1E-3, 2E-3, 5E-3, 1E-2, 2E-2, 5E-2, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000 };
constexpr double SAMPLING_RATE_SINGLE[36] = { 1E9, 1E9, 1E9, 1E9, 1E9, 1E9, 1E9, 500E6, 250E6, 125E6, 50E6, 25E6, 12.5E6, 5E6, 2.5E6, 1.25E6, 500E3, 250E3, 125E3, 50E3, 25E3, 12.5E3, 5E3, 2.5E3, 1.25E3, 500, 250, 125, 50, 25, 12.5, 5, 2.5, 1.25, 0.5, 0.25 };
constexpr double SAMPLING_RATE_DUAL[36] =   { 500E6, 500E6, 500E6, 500E6, 500E6, 500E6, 500E6, 500E6, 250E6, 125E6, 50E6, 25E6, 12.5E6, 5E6, 2.5E6, 1.25E6, 500E3, 250E3, 125E3, 50E3, 25E3, 12.5E3, 5E3, 2.5E3, 1.25E3, 500, 250, 125, 50, 25, 12.5, 5, 2.5, 1.25, 0.5, 0.25 };
constexpr double SAMPLING_RATE_QUAD[36] =   { 250E6, 250E6, 250E6, 250E6, 250E6, 250E6, 250E6, 250E6, 250E6, 125E6, 50E6, 25E6, 12.5E6, 5E6, 2.5E6, 1.25E6, 500E3, 250E3, 125E3, 50E3, 25E3, 12.5E3, 5E3, 2.5E3, 1.25E3, 500, 250, 125, 50, 25, 12.5, 5, 2.5, 1.25, 0.5, 0.25 };
//constexpr int TIME_DIVISIONS = 10;
//0=2mV, 1=5mV, 2=10mV, 3=20mV, 4=50mV, 5=100mV, 6=200mV, 7=500mV, 8=1V, 9=2V, 10=5V, 11=10V (w/ x1 probe)
constexpr int VOLTS_PER_DIVISION = 7; // 500 mV
constexpr double VOLT_MULT[12] = { 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10 };
constexpr int VOLT_DIVISIONS = 8;
constexpr int VOLT_RESOLUTION = 256; //8 bit ADC
constexpr int CH_ZERO_POS[4] = { 128, 128, 128, 128 };

constexpr int PROBE_MULTIPLIER = 1; // 1 or 10 x probe

static WORD calibration_data[CAL_LEVEL_LEN];

static WORD amp_level[AMPCALI_Len];

static short dev_idx = 0; // Initialize to first divice index

short find_and_setup_devs(PCONTROLDATA control_data)
{
    short dev_info[MAX_USB_DEV_NUMBER];
    WORD nr_devs = dsoHTSearchDevice(dev_info);

    ULONG fpga_version = 0,
        hard_version = 0;

    RELAYCONTROL relay_control;

    std::cout << "Found " << nr_devs << " devices" << std::endl;

    // Find the device index number
    for (int i = 0; i < MAX_USB_DEV_NUMBER-1; i++) {
        if(dev_info[i]) {
            dev_idx = i;
            std::cout << "    device: " << dev_info[i] << std::endl;
            break;
        }
    }

    //for (int i = 0; i < 31; i++) {
    //    std::cout << " device: " << dsoHTDeviceConnect(i) << std::endl;
    //}

    // This is broken?
    //if (FALSE == dsoSetUSBBus(dev_idx)) {
    //    std::cout << "Failed to dsoSetUSBBus()" << std::endl;
    //    nr_devs = 0;
    //    goto done;
    //}

    // Check if the device is connected
    if (1 == dsoHTDeviceConnect(dev_idx)) {
        std::cout << "Device is connected!" << std::endl;
    } else {
        std::cerr << "Device connection failure, aborting." << std::endl;
        nr_devs = 0;
        goto done;
    }

    if (0 == dsoInitHard(dev_idx)) {
        std::cerr << "Error while initializing device " << dev_idx << std::endl;
        nr_devs = 0;
        goto done;
    }

    fpga_version = dsoGetFPGAVersion(dev_idx);
    hard_version = dsoGetHardVersion(dev_idx);

    std::cout << "FPGA version: 0x" << std::ios::hex <<  std::setw(8) << std::setfill('0') << fpga_version << " Hardware version: 0x" << hard_version << std::endl;

    //std::cout << "Initializing ADC, press any key to go to the next step" << std::endl;
    //getchar();

    memset(calibration_data, 0, sizeof(calibration_data));
    
    // Set the ADC channel mode (1, 2 or 4)
    if (0 == dsoHTADCCHModGain(dev_idx, ADC_CHANNEL_MODE)) {
        std::cerr << "Failed to set ADC Channel Mod Gain, aborting." << std::endl;
        goto done;
    }

    std::cout << "Set ADC mode to " << ADC_CHANNEL_MODE << ", press any key to continue..." << std::endl;
    //getchar();

    // Read back the calibration data for the device
    if (0 == dsoHTReadCalibrationData(dev_idx, calibration_data, CAL_LEVEL_LEN)) {
        std::cerr << "Failed to read calibration data, aborting." << std::endl;
        goto done;
    }

    //std::cout << "Read back calibration data, press any key to continue..." << std::endl;
    //getchar();

    // Fill the calibration data in with magic numbers iff we don't have valid calibration data
    // Never hit this in my test cases...
    if (calibration_data[CAL_LEVEL_LEN - 1] != ZERO_FLAG) {
        std::cout << "Preparing the calibration data " << std::endl;

        for (size_t i = 0; i < ZEROCALI_LEN; i++) {
            size_t chan = i % ZEROCALI_PER_CH_LEN;
            size_t volt = chan / ZEROCALI_PER_VOLT_LEN;

            if (volt == 5 || volt == 8 || volt == 11) {
                switch (chan % ZEROCALI_PER_VOLT_LEN) {
                case 0:
                    calibration_data[i] = 16602;
                    break;
                case 1:
                    calibration_data[i] = 60111;
                    break;
                case 2:
                    calibration_data[i] = 17528;
                    break;
                case 3:
                    calibration_data[i] = 59201;
                    break;
                case 4:
                    calibration_data[i] = 17710;
                    break;
                case 5:
                    calibration_data[i] = 58900;
                    break;
                default:
                    calibration_data[i] = 0;
                    break;
                }
            }
        }
    }

    // Set  up the "amplifier level" which is probably an amplifier gain
    for (size_t i = 0; i < AMPCALI_Len; i++) {
        amp_level[i] = 1024;
    }

    // Set up the relay control
    memset(reinterpret_cast<void *>(&relay_control), 0, sizeof(relay_control));
    for (size_t i = 0; i <= 3; i++) {
        relay_control.bCHEnable[i] = ENABLED_CHANNELS[i];
        relay_control.nCHVoltDIV[i] = VOLTS_PER_DIVISION;
        relay_control.nCHCoupling[i] = CHANNEL_COUPLING;
        relay_control.bCHBWLimit[i] = 0;
    }
    relay_control.nTrigSource = TRIGGER_CHANNEL;
    relay_control.bTrigFilt = 0;
    relay_control.nALT = 0;

    control_data->nCHSet = CHANS_MASK;
    control_data->nTimeDIV = TIME_PER_DIVISION;
    control_data->nTriggerSource = TRIGGER_CHANNEL;
    control_data->nHTriggerPos = 50;
    control_data->nVTriggerPos = 0;
    control_data->nTriggerSlope = TRIGGER_SLOPE;
    control_data->nBufferLen = BUF_4K_LEN;
    control_data->nReadDataLen = BUF_4K_LEN;
    control_data->nAlreadyReadLen = 0;
    control_data->nALT = 0;

    std::cout << "Setting the DSO Sampling Rate, and normal mode for acquisition" << std::endl;
    if (0 == dsoHTSetSampleRate(dev_idx, YT_NORMAL, &relay_control, control_data)) {
        std::cerr << "Failed to set sample rate, aborting..." << std::endl;
        goto done;
     }

    //NOTE: THE OLDER .DLL HAD THIS EXTRA PARAMETER "amp_level" IN dsoHTSetSampleRate:
    //dsoHTSetSampleRate(dev_idx, amp_level, YT_NORMAL, &relay_control, control_data)

    std::cout << "Setting CH and trigger" << std::endl;
    if (0 == dsoHTSetCHAndTrigger(dev_idx, &relay_control, control_data->nTimeDIV)) {
        std::cerr << "Failed to set relay control and channel details" << std::endl;
        goto done;
    }

    std::cout << "Setting RAM and trigger control" << std::endl;
    if (0 == dsoHTSetRamAndTrigerControl(dev_idx, control_data->nTimeDIV, control_data->nCHSet, control_data->nTriggerSource, 0)) {
        std::cerr << "Failed to set RAM and trigger control" << std::endl;
        goto done;
    }

    std::cout << "Setting each channel zero positions" << std::endl;
    for (int i = 0; i < MAX_CH_NUM; i++) {
        //dsoHTSetCHPos(WORD nDeviceIndex,WORD nVoltDIV,WORD nPos,WORD nCH,WORD nCHMode)
        if (0 == dsoHTSetCHPos(dev_idx, relay_control.nCHVoltDIV[i], CH_ZERO_POS[i], i, ADC_CHANNEL_MODE)) {
            std::cerr << "Failed to set channel position for channel " << i << std::endl;
            goto done;
        }
        std::cout << "CH" << i << " zero is " << CH_ZERO_POS[i] << std::endl;
    }

    // Set the trigger mode
    std::cout << "Set trigger mode to EDGE, DC coupled" << std::endl;
    if (0 == dsoHTSetTrigerMode(dev_idx, TRIGGER_MODE, TRIGGER_SLOPE, TRIGGER_COUPLE)) {
        std::cerr << "Failed to set trigger mode, aborting" << std::endl;
        goto done;
    }
done:
    return nr_devs;
}

int transfer_single_block(uint16_t *ch1, uint16_t *ch2, uint16_t *ch3, uint16_t *ch4, PCONTROLDATA control)
{
    int ret = -1;

    std::cout << "Setting up to transfer a single block..." << std::endl;

    if (1 != dsoHTGetData(dev_idx, ch1, ch2, ch3, ch4, control)) {
        std::cerr << "Failed to get data from DSO, aborting." << std::endl;
        goto done;
    }


    std::cout << "Transferred all 4 channels" << std::endl;
done:
    return ret;
}

int main()
{
    CONTROLDATA control;

    std::cout << "The Hantek Tester" << std::endl;

    memset(&control, 0, sizeof(control));

    find_and_setup_devs(&control);

    ////////////////////////////
    //  SIGNAL GENERATOR (DDS)
    ////////////////////////////
    float frequency = 10E3;
    int amplitude = 1000;
    short offset = 0;
    WORD waveType = 0;

    //Initialize (0=continuous wave, 1=single wave)
    ULONG setCmdResult = ddsSetCmd(dev_idx, 0);
    if (0 == setCmdResult) {
        std::cerr << "Failed to initialize signal generator, aborting." << std::endl;
        return EXIT_FAILURE;
    }
    std::cout << "Initialized DDS for continuous wave, setCmdResult=" << setCmdResult << std::endl;

    //Set Wave Type (0=sine, 1=ramp, 2=square, 4=DC, 8=noise)
    int wtrtn = ddsSDKSetWaveType(dev_idx, waveType);
    std::cout << "Set DDS Weve Type, always returns " << wtrtn << std::endl;

    //Set Frequency
    float frequencyRtn = ddsSDKSetFre(dev_idx, frequency);
    std::cout << "Set DDS Frequency to " << frequencyRtn << std::endl;

    //Set Amplitude
    int amplitudeRtn  = ddsSDKSetAmp(dev_idx, amplitude);
    std::cout << "Set DDS Amplitude to " << amplitudeRtn << std::endl;

    //Set Offset
    short offsetRtn = ddsSDKSetOffset(dev_idx, offset);
    std::cout << "Set DDS Offset to " << offsetRtn << std::endl;

    //Set Enabled
    ddsSetOnOff(dev_idx, 1);
    std::cout << "Enalbed DDS" << std::endl;

    ////////////////////////////
    //    OSCILLOSCOPE (DSO)
    ////////////////////////////
    uint16_t* ch1 = new uint16_t[BUF_4K_LEN];
    uint16_t* ch2 = new uint16_t[BUF_4K_LEN];
    uint16_t* ch3 = new uint16_t[BUF_4K_LEN];
    uint16_t* ch4 = new uint16_t[BUF_4K_LEN];

    memset(ch1, 0, sizeof(uint16_t) * BUF_4K_LEN);
    memset(ch2, 0, sizeof(uint16_t) * BUF_4K_LEN);
    memset(ch3, 0, sizeof(uint16_t) * BUF_4K_LEN);
    memset(ch4, 0, sizeof(uint16_t) * BUF_4K_LEN);

    std::cout << "Attempting to transfer a single block..." << std::endl;

    if (0 == dsoHTStartCollectData(dev_idx, 1)) {
        std::cerr << "Failed to start data collection, aborting." << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "Waiting for transfer readiness" << std::endl;
    while (!(dsoHTGetState(dev_idx) & 0x2));
    std::cout << "Ready to transfer data" << std::endl;

    transfer_single_block(ch1, ch2, ch3, ch4, &control);

    // Create and open a text file
    std::ofstream MyFile("output_data.txt");
    //Write Header
    MyFile << "TIME\tCH1\tCH2\tCH3\tCH4" << std::endl;
    // Write Time and Voltage Data
    for (int i = BUF_4K_LEN - 1; i >= 0; i--) {
        double curSampleRate;
        double curTime;
        double ch1Voltage;
        double ch2Voltage;
        double ch3Voltage;
        double ch4Voltage;
        int ch1Zero = CH_ZERO_POS[0];
        int ch2Zero = CH_ZERO_POS[1];
        int ch3Zero = CH_ZERO_POS[2];
        int ch4Zero = CH_ZERO_POS[3];

        // Calculate Time Points
        if (ADC_CHANNEL_MODE == 1) {
            curSampleRate = SAMPLING_RATE_SINGLE[TIME_PER_DIVISION];
        }
        else if (ADC_CHANNEL_MODE == 2) {
            curSampleRate = SAMPLING_RATE_DUAL[TIME_PER_DIVISION];
        }
        else if (ADC_CHANNEL_MODE == 4) {
            curSampleRate = SAMPLING_RATE_QUAD[TIME_PER_DIVISION];
        }
        else {
            std::cerr << "ADC_CHANNEL_MODE can only be 1, 2 or 4, aborting." << std::endl;
        }
        curTime = i / curSampleRate;
        //curTime = i * TIME_MULT[TIME_PER_DIVISION] * TIME_DIVISIONS / BUF_4K_LEN;
        
        ch1Voltage = (ch1[i] - (255 - ch1Zero)) * PROBE_MULTIPLIER * VOLT_MULT[VOLTS_PER_DIVISION] * VOLT_DIVISIONS / 256;
        ch2Voltage = (ch2[i] - (255 - ch2Zero)) * PROBE_MULTIPLIER * VOLT_MULT[VOLTS_PER_DIVISION] * VOLT_DIVISIONS / 256;
        ch3Voltage = (ch3[i] - (255 - ch3Zero)) * PROBE_MULTIPLIER * VOLT_MULT[VOLTS_PER_DIVISION] * VOLT_DIVISIONS / 256;
        ch4Voltage = (ch4[i] - (255 - ch4Zero)) * PROBE_MULTIPLIER * VOLT_MULT[VOLTS_PER_DIVISION] * VOLT_DIVISIONS / 256;
        
        MyFile << curTime << "\t" << ch1Voltage << "\t" << ch2Voltage << "\t" << ch3Voltage << "\t" << ch4Voltage << std::endl;
    }
     Close the file
    MyFile.close();

    std::cout << "COMPLETED SUCCESSFULLY!!!" << std::endl;

    return EXIT_SUCCESS;
}


