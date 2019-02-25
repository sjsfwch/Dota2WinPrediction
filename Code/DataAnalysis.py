#data analysis
MyKey = "537AD5C3BDCBF53BAFCCA57D016C6514"#steam api keyupdata
import json
import time
import dota2api
import os
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
    print(radiantWin/Sum)

def getHeros():
    '''
    如果英雄文件已经存在，直接打开并返回，否则从steam服务器获取
    '''
    if(os.access("./Data/AnalysisData/heroes.json",os.F_OK)):
        fileHeroes=open("./Data/AnalysisData/heroes.json","r")
        jsonHeroes=json.load(fileHeroes)
        return jsonHeroes
    heroes=api.get_heroes()
    dictHeros={}
    for hero in heroes["heroes"]:
        dictHeros[hero["id"]]=hero["localized_name"]
    sorted(dictHeros.items(),key=lambda x:x[0])
    fileHeroes=open("./Data/AnalysisData/heroes.json","w")
    heroJson=json.dumps(dictHeros,ensure_ascii=False,indent=4)
    fileHeroes.write(heroJson)
    fileHeroes.close()
    return dictHeros


def getHerosStatistics():
    '''
    获取一些英雄的统计信息
    '''
    if(os.access("./Data/AnalysisData/heroesStatistics.json",os.F_OK)):
        fileHeroesStatistics=open("./Data/AnalysisData/heroesStatistics.json","r")
        jsonHeroesStatistics=json.load(fileHeroesStatistics)
        return jsonHeroesStatistics
    #{"id":{"Name":,"WinCount":,"Total":,"WinRate":,"AverageKills":,"AverageDeaths":,"AverageAssists":,"AverageKDA":}}
    HeroesStatisticsDict={} 
    heroesDict=getHeros()
    #初始化字典
    for heroID in heroesDict:
        HeroesStatisticsDict[int(heroID)]={"Name":heroesDict[heroID],"WinCount":0,"Total":0,"WinRate":0,"AverageKills":0,\
            "AverageDeaths":0,"AverageAssists":0,"AverageKDA":0,"AverageGPM":0,"AverageXPM":0}
    RadiantWin,DireWin=0,0
    print(HeroesStatisticsDict)
    for idx in range(1,23):
        fileOb=open("./Data/CleanData/DataWashed"+str(idx)+".JSON","r")
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
                    HeroesStatisticsDict[player["hero_id"]]["WinCount"]+=RadiantWin
                    HeroesStatisticsDict[player["hero_id"]]["Total"]+=1
                else:
                    HeroesStatisticsDict[player["hero_id"]]["WinCount"]+=DireWin
                    HeroesStatisticsDict[player["hero_id"]]["Total"]+=1
                HeroesStatisticsDict[player["hero_id"]]["AverageKills"]+=player["kills"]
                HeroesStatisticsDict[player["hero_id"]]["AverageDeaths"]+=player["deaths"]
                HeroesStatisticsDict[player["hero_id"]]["AverageAssists"]+=player["assists"]
                HeroesStatisticsDict[player["hero_id"]]["AverageGPM"]+=player["gold_per_min"]
                HeroesStatisticsDict[player["hero_id"]]["AverageXPM"]+=player["xp_per_min"]
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
    return HeroesStatisticsDict

if __name__ == '__main__':
    # getHeros()
    getHerosStatistics()
    # analysisWinRateByNone()
