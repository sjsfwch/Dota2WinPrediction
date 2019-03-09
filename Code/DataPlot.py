
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

def heroesWinRate():
    file =open("./Data/AnalysisData/heroesStatistics.json","r")
    dictHeroes=json.load(file)
    winrateList=[]
    for heroes in dictHeroes.values():
        heroes
        winrateList.append(heroes["WinRate"])
    winrateList.sort(reverse=True)
    x=np.arange(len(winrateList))
    plt.bar(x=x,height=winrateList,width=0.5)
    plt.xlabel('胜率排名')
    plt.ylabel('胜率')
    plt.title('全英雄胜率排名')
    plt.show()

def heroesSynergyInfo():
    file = open("./Data/AnalysisData/NewSynergyInfo.json","r")
    dictInfo=json.load(file)
    synergyArr=np.zeros((116,116))
    for heroIdx in dictInfo:
        i=int(heroIdx)-1
        for j in range(0,116):
            if(i==j):
                continue
            synergyArr[i][j]=dictInfo[heroIdx][str(j+1)]
    print(synergyArr)
    cmap = seaborn.cubehelix_palette(start = 1, rot = 3, gamma=1, as_cmap = True)
    seaborn.set_palette("Blues")
    fig=seaborn.heatmap(synergyArr,cmap=cmap)
    fig.invert_yaxis()
    plt.title("英雄配合胜率图")
    plt.xlabel('主英雄序号')
    plt.ylabel('次英雄序号')
    plt.show()


def heroesCounterInfo():
    file = open("./Data/AnalysisData/NewCounterInfo.json","r")
    dictInfo=json.load(file)
    counterArr=np.zeros((116,116))
    for heroIdx in dictInfo:
        i=int(heroIdx)-1
        for j in range(0,116):
            if(i==j):
                continue
            counterArr[i][j]=dictInfo[heroIdx][str(j+1)]

    cmap = seaborn.cubehelix_palette(start = 1.5, rot = 3, gamma=0.8, as_cmap = True)
    fig=seaborn.heatmap(counterArr,cmap=cmap,center=0.5)
    fig.invert_yaxis()
    plt.title("英雄克制胜率图")
    plt.xlabel('主英雄序号')
    plt.ylabel('次英雄序号')
    plt.show()

def lrResult():
    with open("./Data/AnalysisData/LRNorm.json",'r') as file:
        dictRes=json.load(file)
        C=[]
        vecAcc=[]
        vecAccInTrain=[]
        for i in dictRes:
            C.append(float(i))
            vecAcc.append(dictRes[i][0])
            vecAccInTrain.append(dictRes[i][1])
    plt.plot(C,vecAcc,label="交叉验证正确率")
    plt.plot(C,vecAccInTrain,label="训练集正确率",linestyle='--')
    plt.title("正则项系数选取")
    plt.xlabel("正则项系数")
    plt.ylabel("准确率")
    plt.legend(loc='best')
    plt.show()

def rfResult():
    with open("./Data/AnalysisData/RFDepth.json",'r') as file:
        dictRes=json.load(file)
        C=[]
        vecAcc=[]
        vecAccInTrain=[]
        for i in dictRes:
            C.append(i)
            vecAcc.append(dictRes[i][0])
            vecAccInTrain.append(dictRes[i][1])
    plt.plot(C,vecAcc,label="交叉验证正确率")
    plt.plot(C,vecAccInTrain,label="训练集正确率",linestyle='--')
    plt.title("最大深度选取")
    plt.xlabel("最大深度")
    plt.ylabel("准确率")
    plt.legend(loc='best')
    plt.show()

def kNNResult():
    file=open("./Data/AnalysisData/kNNData.json",'r')
    vecK=[x for x in range(3,9)]
    res=[]
    for line in file:
        dictLine=json.loads(line)
        Acc=0
        for i in dictLine:
            Acc+=dictLine[i]
        Acc=round(Acc/10,10)
        res.append(Acc)
    plt.title("Neighbors数量的选取")
    plt.xlabel("Neighbors数量")
    plt.ylabel("准确率")
    plt.plot(vecK,res,label="交叉验证正确率")
    plt.show()

def SVMResult():
    file=open("./Data/AnalysisData/SVMData.json",'r')
    x=[i for i in range(1,11)]
    dictRes=json.load(file)
    vecRes=[dictRes[i] for i in dictRes]
    plt.title("SVM准确率")
    plt.xlabel("次数")
    plt.ylabel("准确率")
    plt.plot(x,vecRes,label="交叉验证正确率")
    plt.show()

def result():
    fileLR=open("./Data/AnalysisData/LRData.json",'r')
    fileRF=open("./Data/AnalysisData/RFData.json",'r')
    filekNN=open("./Data/AnalysisData/kNNData.json",'r')
    fileSVM=open("./Data/AnalysisData/SVMData.json",'r')
    resLRVec=[]
    resRFVec=[]
    reskNNVec=[]
    resSVMVec=[]
    for line in fileLR:
        dictLine=json.loads(line)
        Acc=0
        for i in dictLine:
            Acc+=dictLine[i]
        Acc/=10
        resLRVec.append(Acc)

    for line in fileRF:
        dictLine=json.loads(line)
        Acc=0
        for i in dictLine:
            Acc+=dictLine[i]
        Acc/=10
        resRFVec.append(Acc)

    for line in filekNN:
        dictLine=json.loads(line)
        Acc=0
        for i in dictLine:
            Acc+=dictLine[i]
        Acc/=10
        reskNNVec.append(Acc)

    for line in fileSVM:
        dictLine=json.loads(line)
        Acc=0
        for i in dictLine:
            Acc+=dictLine[i]
        Acc/=10
        resSVMVec.append(Acc)
    resLR=np.sum(resLRVec)/len(resLRVec)
    resRF=np.sum(resRFVec)/len(resRFVec)
    reskNN=np.sum(reskNNVec)/len(reskNNVec)
    resSVM=np.sum(resSVMVec)/len(resSVMVec)
    x=['LR','RF','kNN','SVM']
    y=[resLR,resRF,reskNN,resSVM]
    plt.bar(x,y)
    plt.title("四种算法正确率比较")
    plt.xlabel("算法种类")
    plt.ylabel("平均正确率")
    plt.show()

if __name__ == '__main__':
    # heroesWinRate()
    # heroesSynergyInfo()
    # heroesCounterInfo()
    # SVMResult()
    result()


