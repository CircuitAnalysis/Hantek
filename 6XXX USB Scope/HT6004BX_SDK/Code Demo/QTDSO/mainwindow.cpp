#include "mainwindow.h"
#include "ui_mainwindow.h"
//#include <QLibrary>
#include <QPaintEvent>
#include "../../HeadFiles_UTF8/HTDisplayDll.h"
#define LEFT_MARGIN 16
#define RIGHT_MARGIN 16
#define TOP_MARGIN 16
#define BOTTOM_MARGIN 16
MainWindow::MainWindow(QWidget *parent) :    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    //hard.Init();
    setBackgroundRole(QPalette::Dark);
    setAutoFillBackground(true);
    setAttribute(Qt::WA_PaintOnScreen);
    colletdata.setInterval(500);
    colletdata.start();
    m_GridPixmap=QPixmap(size()-QSize(LEFT_MARGIN+RIGHT_MARGIN,TOP_MARGIN+BOTTOM_MARGIN));
    connect(&colletdata,SIGNAL(timeout()),this,SLOT(timeout()));
}

MainWindow::~MainWindow()
{
    delete ui;
}
void MainWindow::timeout()
{
    if( hard.m_nDeviceIndex==0xFF)  //NO Device
    {
        hard.FindeDev();
        return ;
    }
    hard.ReadData();
    QRect Rect;
    Rect.setLeft(LEFT_MARGIN);
    Rect.setTop(TOP_MARGIN);
    Rect.setSize(size()-QSize(LEFT_MARGIN+RIGHT_MARGIN,TOP_MARGIN+BOTTOM_MARGIN));
    if(hard.m_bDraw)
    {
        update();
    }

}
void MainWindow::DrawWave()
{
    int i = 0;
    HWND hWin=(HWND)this->winId();
    HDC  hDC=GetDC(hWin);
    RECT Rect;
    Rect.left=LEFT_MARGIN;
    Rect.top=TOP_MARGIN;
    Rect.right=Rect.left+size().width()-RIGHT_MARGIN-LEFT_MARGIN;
    Rect.bottom=Rect.top+size().height()-BOTTOM_MARGIN-TOP_MARGIN;
   // Rect.setSize(size()-QSize(LEFT_MARGIN+RIGHT_MARGIN,TOP_MARGIN+BOTTOM_MARGIN));
    DrawGrid(hDC,Rect);
    for(i=0;i<4;i++)
    {
        DrawWaveInYT(hDC,Rect,i);
    }
}

void MainWindow::DrawWaveInYT(HDC hDC,RECT Rect,USHORT nCH)
{
    short* pData = hard.m_pSrcData[nCH];//源数据
    ULONG nDisDataLen = 2500;//网格内要画的数据长度
    ULONG nSrcDataLen = BUF_4K_LEN;//源数据的长度
    //USHORT nDisLeverPos = 128;//m_pDoc->m_Hard.m_nLeverPos[nCH];//零电平的显示位置

    COLORREF clrRGB = hard.m_clrRGB[nCH];//颜色
   // USHORT nHTriggerPos = hard.m_stControl.nHTriggerPos;//水平触发点位置
    ULONG nCenterData = hard.m_stControl.nHTriggerPos/100.0*nSrcDataLen;//
    USHORT nYTFormat = 0;//YT模式
    USHORT nDisType = 0;//显示类型，点或线
    double dbVertical = 1.0;//垂直放大系数
    double dbHorizontal = 1.0;//水平放大系数

    HTDrawWaveInYT(hDC,Rect,clrRGB,nDisType,hard.m_pSrcData[nCH],nSrcDataLen,nDisDataLen,nCenterData,hard.m_nLeverPos[nCH],dbHorizontal,dbVertical,nYTFormat,0);
}

void MainWindow::DrawGrid(HDC hDC,RECT Rect)
{
    //画网格
    USHORT nHoriGridNum=10;//Hori  Div number
     USHORT nVertGridNum=8;//Vert  Div number
     USHORT nBright=200;
     USHORT IsGrid=1;
    HTDrawGrid(hDC,Rect.left,Rect.top,Rect.right,Rect.bottom,nHoriGridNum,nVertGridNum,nBright,IsGrid);
}
void MainWindow::paintEvent(QPaintEvent *e)
{
    if(hard.m_bDraw)
    {
        DrawWave();
        hard.m_bDraw=false;
        hard.m_bStartC=true;
    }
    {
        e->ignore();
    }
}
void MainWindow::resizeEvent(QResizeEvent *e)
{
    DrawWave();
}
