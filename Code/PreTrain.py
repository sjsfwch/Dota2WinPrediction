import json
import csv
import os
from DataAnalysis import getSynergyInfo,getCounterInfo,getHeroes
import numpy as np

def buildDatasetCsv():
    if(os.access("./Data/AnalysisData/dataset.csv",os.F_OK)):
        return
    synergyDict=getSynergyInfo()
    counterDict=getCounterInfo()
    dataset=open("./Data/CleanData/DataSet.json","r")
    datasetCsv=open("./Data/AnalysisData/dataset.csv","w",newline='',encoding="utf-8")
    writter=csv.writer(datasetCsv)
    # 1-116为1则表示编号为i的英雄在天辉 117-233为1表示编号为i-116的英雄在夜宴 第0列表示天辉赢没赢
    datasetHead=[]
    datasetHead.append("天辉赢")
    heroes=getHeroes()
    HeroIDToSeq=heroes["HeroIDToSeq"]
    for i in range(1,117):
        datasetHead.append("天辉"+heroes[str(i)])
    for i in range(117,233):
        datasetHead.append("夜宴"+heroes[str(i-116)])
    datasetHead.append("协同")
    datasetHead.append("克制")
    writter.writerow(datasetHead)
    lines=dataset.readlines()
    for line in lines:
        game=json.loads(line)
        gameArr=[0 for i in range(0,233)]
        #天辉协同，夜宴协同，克制关系
        SR,SD,C=0,0,0
        if(game["radiant_win"]):
            gameArr[0]=1
        for i in range(0,10):
            player1=game["players"][i]
            for j in range(0,10):
                if(i==j):
                    continue
                player2=game["players"][j]
                # 在天辉
                if(player1["player_slot"]<128):
                    gameArr[HeroIDToSeq[str(player1["hero_id"])]]=1
                    # 两个都在天辉，计算天辉协同
                    if(player2["player_slot"]<128):
                        SR+=synergyDict[str(HeroIDToSeq[str(player1["hero_id"])])][str(HeroIDToSeq[str(player2["hero_id"])])]
                    # 一天辉，一夜宴，计算天辉对夜宴的克制关系
                    else:
                        C+=counterDict[str(HeroIDToSeq[str(player1["hero_id"])])][str(HeroIDToSeq[str(player2["hero_id"])])]-0.5
                else:
                    gameArr[HeroIDToSeq[str(player1["hero_id"])]+116]=1
                    # 两个都在夜宴，计算夜宴协同
                    if(player2["player_slot"]>=128):
                        SD+=synergyDict[str(HeroIDToSeq[str(player1["hero_id"])])][str(HeroIDToSeq[str(player2["hero_id"])])]
        gameArr.append(SR-SD)
        gameArr.append(C)
        writter.writerow(gameArr)

if __name__ == '__main__':
    buildDatasetCsv()