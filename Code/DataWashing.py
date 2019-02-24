#washing the data

# {
# 	"radiant_win":0/1
# 	"radiant_score": 
#   "dire_score": 
# 	"tower_status_radiant": 
# 	"tower_status_dire": 
# 	"barracks_status_radiant": 
# 	"barracks_status_dire": 
# 	"game_mode":1,2,3
# 	"lobby_type":0,2,5,7
# 	"duration":
# 	"players":[
# 			{
# 				"player_slot": 0,
#             			"hero_id": 76,
# 				"gold_per_min": 172,
#             			"xp_per_min": 119,
# 				"last_hits"
# 				"leaver_status":0,1
# 			}
# 		]
# }

import json


def washData(data):
    Dict={}
    #有人掉线且没连回来的比赛丢弃，不需要
    Dict["radiant_win"]=data["radiant_win"]
    Dict["radiant_score"]=data["radiant_score"]
    Dict["dire_score"]=data["dire_score"]
    Dict["tower_status_radiant"]=data["tower_status_radiant"]
    Dict["tower_status_dire"]=data["tower_status_dire"]
    Dict["barracks_status_radiant"]=data["barracks_status_radiant"]
    Dict["barracks_status_dire"]=data["barracks_status_dire"]
    Dict["game_mode"]=data["game_mode"]
    Dict["lobby_type"]=data["lobby_type"]
    Dict["duration"]=data["duration"]
    #少于25分钟的比赛没有意义
    if(data["duration"]<1500):
        return {}
    players=[]
    for player in data["players"]:
        playerAW={}
        #没掉线或者掉线后95分钟内连回来了
        if ('leaver_status' in player.keys()):
            if(player["leaver_status"]==0 or player["leaver_status"]==1):
                playerAW["player_slot"]=player["player_slot"]
                playerAW["hero_id"]=player["hero_id"]
                playerAW["gold_per_min"]=player["gold_per_min"]
                playerAW["xp_per_min"]=player["xp_per_min"]
                playerAW["last_hits"]=player["last_hits"]
                playerAW["leaver_status"]=player["leaver_status"]
            else:
                return {}
        #否则弃掉该条数据
        else:
            return {}
        players.append(playerAW)
    Dict["players"]=players
    return Dict
    
        
def washing():
    count=0
    fileCount=1
    dataWashed=open("F:/dota2win/Dota2WinPrediction/Data/CleanData/DataWashed"+str(fileCount)+".JSON","w")
    fileCount+=1
    for idx in range (1,3001,1):
        file=open("F:/dota2win/Dota2WinPrediction/Data/RawData/TrainData"+str(idx)+".JSON","r")
        lines=file.readlines()
        for line in lines:
            todict=json.loads(line)
            dictAfterWashing={}
            #只要全阵营选择，随机征召，队长模式的比赛。也只要匹配，队伍匹配，锦标赛，天梯模式的比赛
            if((todict["game_mode"]==1 or todict["game_mode"]==2 or todict["game_mode"]==3) and (todict["lobby_type"]==0 or \
                todict["lobby_type"]==2 or todict["lobby_type"]==5 or todict["lobby_type"]==7) ):  
                dictAfterWashing=washData(todict)
            #若传回的是空字典，则说明有人掉线，数据被抛弃
            if(dictAfterWashing):
                tojson=json.dumps(dictAfterWashing)
                dataWashed.write(tojson+'\n')
                #记录该文件写了多少数据了
                count+=1
                #一个文件最多存10000条，写满就写下一个文件
                if (count==10000):
                    dataWashed.close()
                    dataWashed=open("F:/dota2win/Dota2WinPrediction/Data/CleanData/DataWashed"+str(fileCount)+".JSON","w")
                    fileCount+=1
                    count=0
        file.close()
        print("当前进度：%.1f"%(idx/30))


if __name__ == '__main__':
    washing()
    # file=open("F:/dota2win/Dota2WinPrediction/Data/TrainData.JSON","r")
    # dataWashed=open("F:/dota2win/Dota2WinPrediction/Data/DataWashed.JSON","w")
    # lines=file.readlines()
    # for line in lines:
    #     todict=json.loads(line)
    #     #只要全阵营选择，随机征召，队长模式的比赛。也只要匹配，队伍匹配，锦标赛，天梯模式的比赛
    #     if(todict["game_mode"]==1 or todict["game_mode"]==2 or todict["game_mode"]==3 or todict["lobby_type"]==0 or \
    #        todict["lobby_type"]==2 or todict["lobby_type"]==5 or todict["lobby_type"]==7 ):  
    #         dictAfterWashing=washData(todict)
    #     #若传回的是空字典，则说明有人掉线，数据被抛弃
    #     if(dictAfterWashing):
    #         tojson=json.dumps(dictAfterWashing)
    #         dataWashed.write(tojson+'\n')
    # file.close()
    # dataWashed.close()



