#data analysis
import json
def analysis():
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


if __name__ == '__main__':
    analysis()