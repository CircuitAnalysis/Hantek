#ifndef _HT_SCOPE_DEFINE_MACRO_H
#define _HT_SCOPE_DEFINE_MACRO_H

#define MAX_TIMEDIV_NUM				36	//总时基档位个数		
#define TIMEDIV_OFFSET				2	//时基偏移量

#define DRIVERVERLEN	8//必须为偶数
#define AUTOSET_TIME1 19
#define AUTOSET_TIME2 18
#define ZERO_START_VOLT 5
#define BUF_10K_LIMIT			

#define	PI							3.14159265358979323846


#define BUF_4K_LEN					0x1000
#define BUF_3K_LEN					0x0C00//3072
#define BUF_8K_LEN					0x2000
#define BUF_16K_LEN					0x4000
#define BUF_32K_LEN					0x8000
#define BUF_64K_LEN					0x10000

#define BUF_INSERT_LEN 				BUF_72K_LEN	


#define DEF_READ_DATA_LEN			BUF_4K_LEN //BUF_10K_LEN		//默认读取的数据长度
#define DEF_DRAW_DATA_LEN			2500 //10000			


#define MAX_INSERT_TIMEDIV			6	//200nS	最大需要插值的时基 
#define MAX_DOUBLE_TIMEDIV			MAX_INSERT_TIMEDIV
#define MAX_SF_T_TIMEDIV			MAX_INSERT_TIMEDIV - 2  //需要软件找触发的时基
#define MAX_SINE_TIMEDIV			3////2////2  //小于3必须正弦插值




#define MIN_SCAN_TIMEDIV			25//22				//扫描模式最小时基
#define MIN_ROLL_TIMEDIV			27//24				//
#define MIN_ROLL_TIMEDIV			27//24				//



#define SINE_WAVE_LEN				128				//中间小窗口的波形长度
#define MAX_ETS_TIMEDIV				3		//0,1,2,3
#define ETS_SAMPLING_100M			0		//ETS 100M

//基准电平的9点校准*********************************************/
#define NEW_CAL_LEVEL_LEN			400		//1*9+9*(4*9)=334		//首个点为9代表9点校准发


//垂直***********************************************************/
//定义CH
#define CH1							0
#define CH2							1
#define CH3							2
#define CH4							3

#define MAX_CH_NUM				4


#define HORIZONTAL					MAX_CH_NUM		//CH1/CH2/CH3/CH4/HORIZONTAL/(水平lever)
#define MATH						MAX_CH_NUM		//CH1/CH2/CH3/CH4/MATH/REF (垂直lever)
#define REF							MAX_CH_NUM+1	//CH1/CH2/CH3/CH4/MATH/REF (垂直lever)
#define ALL_CH						MAX_CH_NUM+2
#define MIN_DATA						0				//
#define MAX_DATA					255				//
#define MID_DATA					128				//
#define MAX_VOLTDIV_NUM				12

#define YT							0
#define XY							1
#define YT_NORMAL					0
#define YT_SCAN						1
#define YT_ROLL						2

#define DC							0
#define AC							1
#define GND							2


//触发***********************************************************/
#define MAX_TRIGGER_SOURCE_NUM		MAX_CH_NUM+2	//CH1/CH2/CH3/CH4/EXT/(EXT/10)
#define MAX_ALT_TRIGGER_NUM			MAX_CH_NUM+2		//CH1/CH2/CH3/CH4
#define EXT							MAX_CH_NUM		
#define EXT10						MAX_CH_NUM + 1	

#define EDGE						0
#define PULSE						1
#define VIDEO						2
#define CAN							3
#define LIN							4
#define UART						5
#define SPI							6
#define IIC							7

#define FORCE						0x80


#define AUTO						0
#define NORMAL						1
#define SINGLE						2

#define RISE						0
#define FALL						1

//结构体
typedef struct _HT_MEASURE_ITEM
{
	int Enable;
	short nSource;
	short nType;
}HT_MEASURE_ITEM, *PHT_MEASURE_ITEM;
//
struct CAN_DECODE
{
	unsigned char nInfo;
	unsigned char nAck;
	unsigned char nEOF;
	//unsigned char pCRC[3];
	unsigned char pData[8];
	unsigned short nReadCRC;
	unsigned short nCalCRC;
	unsigned short nStartIndex;
	unsigned short nEndIndex;
	unsigned int nID;
};
struct LIN_DECODE
{
	unsigned char  nID;
	unsigned char pData[8];
	unsigned char nReadCRC;
	unsigned char nCalCRC;
	unsigned short nStartIndex;
	unsigned short nEndIndex;

};
struct IIC_DECODE
{
	unsigned char nData;
	unsigned char nType;
	unsigned char nAck;
	unsigned short nStartIndex;
	unsigned short nEndIndex;
};
struct UART_DECODE
{
	unsigned char nData;
	unsigned short nStartIndex;
	unsigned short nEndIndex;
};
struct SPI_DECODE
{
	unsigned char nData[4];
	unsigned short nStartIndex;
	unsigned short nEndIndex;
};

//
typedef struct _HT_DATA_MATCH
{
	unsigned short nTimeDIV;//时基
	unsigned short nVoltDIV;//电压档位
	unsigned short nLeverPos;//零电平位置
	long nHTriggerPos;//水平触发点
	unsigned int nReadDataLen;//读取的数据长度
	unsigned int nAlreadyReadLen;//已经读取的数据长度
}DATAMATCH, *PDATAMATCH;

typedef struct _HT_RELAY_CONTROL
{
	unsigned int bCHEnable[MAX_CH_NUM];
	unsigned short nCHVoltDIV[MAX_CH_NUM];
	unsigned short nCHCoupling[MAX_CH_NUM];
	unsigned int bCHBWLimit[MAX_CH_NUM];
	unsigned short nTrigSource;
	unsigned int bTrigFilt;
	unsigned short nALT;
}RELAYCONTROL, *PRELAYCONTROL;
typedef struct _HT_CONTROL_DATA
{
	unsigned short nCHSet;
	unsigned short nTimeDIV;
	unsigned short nTriggerSource;
	unsigned short nHTriggerPos;
	unsigned short nVTriggerPos;
	unsigned short nTriggerSlope;
	unsigned int nBufferLen;//对应于10K，1M，2M.....16M
	unsigned int nReadDataLen;//记录本次将要从硬件读取的数据总共长度
	unsigned int nAlreadyReadLen;//记录本次已经读取的数据长度，在扫描/滚动模式下有效,在NORMAL模式下无效
	unsigned short nALT;
	unsigned short nETSOpen;
	unsigned short nDriverCode;		//驱动编号
	unsigned int nLastAddress;  //    记录扫描模式上次读取的终止地址
	unsigned short nFPGAVersion;//FPGA 版本号
	//unsigned short nAddressOffset;//触发抖动加偏移


}CONTROLDATA, *PCONTROLDATA;







//
#define MAX_DRIVER_NAME				64		//最大设备名称长度
#define USB_PACK_SIZE				512		//USB上传数据包大小



///////////////////////////////////////////////////
#endif
