#data analysis
MyKey = "537AD5C3BDCBF53BAFCCA57D016C6514"#steam api keyupdata
import json
import time
import dota2api
import os
import numpy as np
api = dota2api.Initialise(api_key=MyKey,language='zh_CN')
def analysisWinRateByNone():
    Sum=0
    radiantWin=0
    for i in range(1,23):
        file=open("F:/dota2win/Dota2WinPrediction/Data/CleanData/DataWashed"+str(i)+".JSON","r")
        lines=file.readlines()
        for line in lines:
            todict=json.loads(line)
            Sum+=1
            if(todict["radiant_win"]):
                radiantWin+=1

def getHeroes():
    '''
    如果英雄文件已经存在，直接打开并返回，否则从steam服务器获取
    '''
    if(os.access("./Data/AnalysisData/heroes.json",os.F_OK)):
        fileHeroes=open("./Data/AnalysisData/heroes.json","r")
        jsonHeroes=json.load(fileHeroes)
        return jsonHeroes
    heroes=api.get_heroes()
    dictHeroes={}
    # 因为英雄id不是连续的，不方便后续的分析，建立一个英雄id到顺序排序的映射
    HeroIDToSeq={}
    i=1
    for hero in heroes["heroes"]:
        dictHeroes[i]=hero["localized_name"]
        HeroIDToSeq[hero["id"]]=i
        i+=1   
    dictHeroes["HeroIDToSeq"]=HeroIDToSeq
    fileHeroes=open("./Data/AnalysisData/heroes.json","w")
    heroJson=json.dumps(dictHeroes,ensure_ascii=False,indent=4)
    fileHeroes.write(heroJson)
    fileHeroes.close()
    fileHeroes=open("./Data/AnalysisData/heroes.json","r")
    jsonHeroes=json.load(fileHeroes)
    return jsonHeroes


def getHeroesStatistics():
    '''
    获取一些英雄的统计信息
    '''
    if(os.access("./Data/AnalysisData/heroesStatistics.json",os.F_OK)):
        fileHeroesStatistics=open("./Data/AnalysisData/heroesStatistics.json","r")
        jsonHeroesStatistics=json.load(fileHeroesStatistics)
        return jsonHeroesStatistics
    #{"id":{"Name":,"WinCount":,"Total":,"WinRate":,"AverageKills":,"AverageDeaths":,"AverageAssists":,"AverageKDA":}}
    HeroesStatisticsDict={} 
    HeroesDict=getHeroes()
    HeroIDToSeq=HeroesDict["HeroIDToSeq"]
    #初始化字典
    for heroSeqID in range(1,len(HeroIDToSeq)+1):
        HeroesStatisticsDict[heroSeqID]={"Name":HeroesDict[str(heroSeqID)],"WinCount":0,"Total":0,"WinRate":0,"AverageKills":0,\
            "AverageDeaths":0,"AverageAssists":0,"AverageKDA":0,"AverageGPM":0,"AverageXPM":0}
    RadiantWin,DireWin=0,0
    with open("./Data/CleanData/NewDataSet.JSON","r") as fileOb:
        lines=fileOb.readlines()
        for line in lines:
            dictLine=json.loads(line)
            if(dictLine["radiant_win"]):
                RadiantWin,DireWin=1,0
            else:
                RadiantWin,DireWin=0,1
            for player in dictLine["players"]:
                #天辉方
                if(player["player_slot"]<128):
                    HeroesStatisticsDict[HeroIDToSeq[str(player["hero_id"])]]["WinCount"]+=RadiantWin
                    HeroesStatisticsDict[HeroIDToSeq[str(player["hero_id"])]]["Total"]+=1
                else:
                    HeroesStatisticsDict[HeroIDToSeq[str(player["hero_id"])]]["WinCount"]+=DireWin
                    HeroesStatisticsDict[HeroIDToSeq[str(player["hero_id"])]]["Total"]+=1
                HeroesStatisticsDict[HeroIDToSeq[str(player["hero_id"])]]["AverageKills"]+=player["kills"]
                HeroesStatisticsDict[HeroIDToSeq[str(player["hero_id"])]]["AverageDeaths"]+=player["deaths"]
                HeroesStatisticsDict[HeroIDToSeq[str(player["hero_id"])]]["AverageAssists"]+=player["assists"]
                HeroesStatisticsDict[HeroIDToSeq[str(player["hero_id"])]]["AverageGPM"]+=player["gold_per_min"]
                HeroesStatisticsDict[HeroIDToSeq[str(player["hero_id"])]]["AverageXPM"]+=player["xp_per_min"]
    for i in HeroesStatisticsDict:
        HeroesStatisticsDict[i]["WinRate"]=round(HeroesStatisticsDict[i]["WinCount"]/HeroesStatisticsDict[i]["Total"],4)
        HeroesStatisticsDict[i]["AverageKills"]=round(HeroesStatisticsDict[i]["AverageKills"]/HeroesStatisticsDict[i]["Total"],1)
        HeroesStatisticsDict[i]["AverageDeaths"]=round(HeroesStatisticsDict[i]["AverageDeaths"]/HeroesStatisticsDict[i]["Total"],1)
        HeroesStatisticsDict[i]["AverageAssists"]=round(HeroesStatisticsDict[i]["AverageAssists"]/HeroesStatisticsDict[i]["Total"],1)
        HeroesStatisticsDict[i]["AverageGPM"]=round(HeroesStatisticsDict[i]["AverageGPM"]/HeroesStatisticsDict[i]["Total"],1)
        HeroesStatisticsDict[i]["AverageXPM"]=round(HeroesStatisticsDict[i]["AverageXPM"]/HeroesStatisticsDict[i]["Total"],1)
        HeroesStatisticsDict[i]["AverageKDA"]=round((HeroesStatisticsDict[i]["AverageKills"]+HeroesStatisticsDict[i]["AverageAssists"])\
            /( HeroesStatisticsDict[i]["AverageDeaths"] if HeroesStatisticsDict[i]["AverageDeaths"]!=0 else 1),1)
    fileHeroesStatistics=open("./Data/AnalysisData/heroesStatistics.json","w")
    jsonHeroesStatistics=json.dumps(HeroesStatisticsDict,ensure_ascii=False,indent=4)
    fileHeroesStatistics.write(jsonHeroesStatistics)
    fileHeroesStatistics.close()
    fileHeroesStatistics=open("./Data/AnalysisData/heroesStatistics.json","r")
    jsonHeroesStatistics=json.load(fileHeroesStatistics)
    return jsonHeroesStatistics

def buildSynergyAndCounterInfo():
    '''
    获取两个英雄的协同和克制信息，即谁和谁一起胜率高
    '''
    heroes=getHeroes()
    heroesNum=len(heroes)-1
    print(heroesNum)
    HeroIDToSeq=heroes["HeroIDToSeq"]
    # 注意深浅拷贝
    synergyArr=np.zeros((heroesNum+1,heroesNum+1))
    synergyArrSum=np.zeros((heroesNum+1,heroesNum+1))
    counterArr=np.zeros((heroesNum+1,heroesNum+1))
    counterArrSum=np.zeros((heroesNum+1,heroesNum+1))
    for i in range(1,heroesNum+1):
        synergyArr[i][0],synergyArr[0][i]=i,i
        synergyArrSum[i][0],synergyArrSum[0][i]=i,i
        counterArr[i][0],counterArr[0][i]=i,i
        counterArrSum[i][0],counterArrSum[0][i]=i,i
    
    # synergyArr[i][j]表示玩i时队友有j的胜率
    # counterArr[i][j]表示玩i时对面有j的胜率
    for idx in range(1,23):
        fileOb=open("./Data/CleanData/DataWashed"+str(idx)+".JSON","r")
        lines=fileOb.readlines()
        for line in lines:
            dictLine=json.loads(line)
            if(dictLine["radiant_win"]):
                RadiantWin,DireWin=1,0
            else:
                RadiantWin,DireWin=0,1
            for i in range(0,len(dictLine["players"])):
                for j in range(0,len(dictLine["players"])):
                    # 自己跟自己不算
                    if(i==j):
                        continue
                    MyID=HeroIDToSeq[str(dictLine["players"][i]["hero_id"])]
                    OtherID=HeroIDToSeq[str(dictLine["players"][j]["hero_id"])]
                    # 玩的天辉方
                    if(dictLine["players"][i]["player_slot"]<128):
                        # 队友
                        if(dictLine["players"][j]["player_slot"]<128):
                            synergyArr[MyID][OtherID]+=RadiantWin
                            synergyArrSum[MyID][OtherID]+=1
                        # 敌人
                        else:
                            counterArr[MyID][OtherID]+=RadiantWin
                            counterArrSum[MyID][OtherID]+=1
                    # 玩的夜宴方
                    else:
                        # 敌人
                        if(dictLine["players"][j]["player_slot"]<128):
                            counterArr[MyID][OtherID]+=DireWin
                            counterArrSum[MyID][OtherID]+=1
                        # 队友
                        else:
                            synergyArr[MyID][OtherID]+=DireWin
                            synergyArrSum[MyID][OtherID]+=1
    synergyInfo={}
    counterInfo={}
    for i in range(1,heroesNum+1):
        synergyInfo[i]={}
        counterInfo[i]={}
        for j in range(1,heroesNum+1):
            if(i==j):
                continue
            synergyArr[i][j]=round(synergyArr[i][j]/synergyArrSum[i][j],4)
            counterArr[i][j]=round(counterArr[i][j]/counterArrSum[i][j],4)
            synergyInfo[i][j]=synergyArr[i][j]
            counterInfo[i][j]=counterArr[i][j]
    fileSynergy=open("./Data/AnalysisData/synergyInfo.json","w")
    fileCounter=open("./Data/AnalysisData/counterInfo.json","w")
    fileSynergy.write(json.dumps(synergyInfo,indent=4))
    fileCounter.write(json.dumps(counterInfo,indent=4))

def getSynergyInfo():
    if(not os.access("./Data/AnalysisData/NewSynergyInfo.json",os.F_OK)):
        buildSynergyAndCounterInfo()
    fileSynergy=open("./Data/AnalysisData/NewSynergyInfo.json","r")
    return json.load(fileSynergy)

def getCounterInfo():
    if(not os.access("./Data/AnalysisData/NewCounterInfo.json",os.F_OK)):
        buildSynergyAndCounterInfo()
    fileCounter=open("./Data/AnalysisData/NewCounterInfo.json","r")
    return json.load(fileCounter)

def buildDataset():
    # 如果已经建好了 就直接返回
    if(os.access("./Data/CleanData/DataSet.json",os.F_OK)):
        return
    dataset=open("./Data/CleanData/DataSet.json","w")
    for idx in range(1,23):
        fileOb=open("./Data/CleanData/DataWashed"+str(idx)+".JSON","r")
        lines=fileOb.readlines()
        for line in lines:
            dataset.write(line)
    dataset.close()

if __name__ == '__main__':
    # getHeroes()
    getHeroesStatistics()
    # buildSynergyAndCounterInfo()
    # buildDataset()
    # analysisWinRateByNone()
