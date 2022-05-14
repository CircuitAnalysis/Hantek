#include "Hard.h"
//#include <QLibrary>
#include <QMessageBox>
Hard::Hard()
{

    m_bDraw=false;
    m_bStartC=true;
    ULONG i = 0;
    m_nDeviceIndex = 0xFF;
    m_nDeviceNum = 0;
    for(i=0;i<MAX_CH_NUM;i++)
    {
        m_pSrcData[i] = new short[BUF_4K_LEN];
    }
    m_clrRGB[CH1] = RGB(255,255,0);
    m_clrRGB[CH2] = RGB(0,255,255);
    m_clrRGB[CH3] = RGB(255,0,255);
    m_clrRGB[CH4] = RGB(0,255,0);
    m_nTimeDIV = 9;
    m_nYTFormat = YT_NORMAL;
    m_stControl.nCHSet = 0x0F;////Factory Setup
    m_stControl.nTimeDIV = m_nTimeDIV;//Factory Setup
    m_stControl.nTriggerSource = CH1;//Factory Setup
    m_stControl.nHTriggerPos = 50;//Factory Setup
    m_stControl.nVTriggerPos = 64;//Factory Setup
    m_stControl.nTriggerSlope = RISE;//Factory Setup
    m_stControl.nBufferLen = BUF_4K_LEN;//Factory Setup
    m_stControl.nReadDataLen = BUF_4K_LEN;//Factory Setup
    m_stControl.nAlreadyReadLen = BUF_4K_LEN;//Factory Setup
    m_stControl.nALT = 0;//Factory Setup
    m_stControl.nFPGAVersion = 0xa000;//Factory Setup
    for(i=0;i<MAX_CH_NUM;i++)
    {
        RelayControl.bCHEnable[i] = 1;
        RelayControl.nCHVoltDIV[i] = 5;
        RelayControl.nCHCoupling[i] = AC;
        RelayControl.bCHBWLimit[i] = 0;
    }
    RelayControl.nTrigSource = CH1;
    RelayControl.bTrigFilt = 0;
    RelayControl.nALT = 0;
    m_nTriggerMode = EDGE;
    m_nTriggerSlope = RISE;
    m_nTriggerSweep = AUTO;
    m_nLeverPos[CH1] = 192;
    m_nLeverPos[CH2] = 160;
    m_nLeverPos[CH3] = 96;
    m_nLeverPos[CH4] = 64;

    m_bCollect=TRUE;
    m_nReadOK = 0;
}
short Hard::FindeDev()
{
    for(m_nDeviceIndex=0;m_nDeviceIndex<32;m_nDeviceIndex++)
    {
        if(dsoHTDeviceConnect(m_nDeviceIndex))
        {
            Init();
            return 1;
        }
    }
    m_nDeviceIndex=0xFF;
    return 0;

}
void Hard::Init()
{

    //m_nDeviceIndex = 0;
    short n=dsoInitHard(m_nDeviceIndex);//硬件初始化
    dsoHTADCCHModGain(m_nDeviceIndex, 4);//设置由通道模式引起的幅度修正

    dsoHTSetSampleRate(m_nDeviceIndex, m_nYTFormat, &RelayControl, &m_stControl);//设置采样率
    dsoHTSetCHAndTrigger(m_nDeviceIndex, &RelayControl, m_stControl.nTimeDIV);//设置通道开关和电压档位
    dsoHTSetRamAndTrigerControl(m_nDeviceIndex, m_stControl.nTimeDIV, m_stControl.nCHSet, m_stControl.nTriggerSource, 0);//设置触发源
    for (WORD i = 0; i < MAX_CH_NUM; i++)
    {
        dsoHTSetCHPos(m_nDeviceIndex, RelayControl.nCHVoltDIV[i], m_nLeverPos[i], i, 4);
    }
    dsoHTSetVTriggerLevel(m_nDeviceIndex, m_nLeverPos[CH1], 4);
    switch (m_nTriggerMode) {//触发设置
    case EDGE:
        dsoHTSetTrigerMode(m_nDeviceIndex, m_nTriggerMode, m_stControl.nTriggerSlope, DC);
        break;

    default:
        break;
    }
}


void Hard::SourceToDisplay(USHORT* pData,ULONG nDataLen,USHORT nCH)
{
    for(int i=0;i<nDataLen;i++)
    {
        *(m_pSrcData[nCH]+i) = *(pData+i)-(MAX_DATA - m_nLeverPos[nCH]);
    }
}
WORD Hard::startAStatus()
{
     if(m_bStartC)
    {
        dsoHTStartCollectData(m_nDeviceIndex,(WORD)1);
        m_bStartC=false;
        return 0;
    }
   return  dsoHTGetState(m_nDeviceIndex);
}
void Hard::ReadData()
{

    WORD nTmep=startAStatus();
    if(nTmep<2)
        return;
    int i=0;
    USHORT* pReadData[MAX_CH_NUM];
    for(i=0;i<MAX_CH_NUM;i++)
    {
        pReadData[i] = new USHORT[m_stControl.nReadDataLen];
        memset(pReadData[i],0,m_stControl.nReadDataLen*sizeof(USHORT));
    }
    dsoHTGetData(m_nDeviceIndex,pReadData[CH1],pReadData[CH2],pReadData[CH3],pReadData[CH4],&m_stControl);
    m_bDraw=true;
    for(WORD i=0;i<MAX_CH_NUM;i++)
    {
        SourceToDisplay(pReadData[i],m_stControl.nReadDataLen,i);
    }
    for(i=0;i<MAX_CH_NUM;i++)
    {
        delete pReadData[i];
    }
}
