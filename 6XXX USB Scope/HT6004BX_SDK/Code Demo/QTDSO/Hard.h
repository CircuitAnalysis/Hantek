#ifndef HARD_H
#define HARD_H
#include "../../HeadFiles_UTF8/HTHardDll.h"

#include <windows.h>
#include "../../HeadFiles_UTF8/DefMacro.h"



class Hard
{

public:
    Hard();
    short FindeDev();
    void Init();
    void ReadData();
    WORD startAStatus();
    void SourceToDisplay(USHORT* pData,ULONG nDataLen,USHORT nCH);
public:
    bool m_bDraw;
    bool m_bStartC;
    USHORT m_nDeviceIndex;
    USHORT m_nDeviceNum;
    short* m_pSrcData[MAX_CH_NUM];//读取的数据减去零电平的位置(-255 ~ 255)
    USHORT m_nTimeDIV;
    USHORT m_nYTFormat;
    BOOL m_bCollect;
    CONTROLDATA m_stControl;
    RELAYCONTROL RelayControl;
    USHORT m_nTriggerMode;
    USHORT m_nTriggerSweep;
    USHORT m_nTriggerSlope;
    USHORT m_nLeverPos[MAX_CH_NUM];
    COLORREF m_clrRGB[MAX_CH_NUM];
    USHORT m_nReadOK;//本次读数据是否正确,0,不正确；非0不正确。
};

#endif // HARD_H
