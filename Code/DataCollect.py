MyKey = "537AD5C3BDCBF53BAFCCA57D016C6514"
China = [161, 163, 221, 222, 223, 224, 225, 231]
import time
import json
import dota2api
seqnum = 3752089975
api = dota2api.Initialise(MyKey)
#ma=api.get_match_details(match_id=4324781398)

success=1
for jsonnIdex in range(1,1001,1):
    if(success==0):
        break
    fileJson=open("F:/dota2win/Dota2WinPrediction/Data/TrainData" + str(jsonnIdex) + ".JSON", "w")
    i=1
    while(i<=10):
        try:
            datas=api.get_match_history_by_seq_num(start_at_match_seq_num=seqnum)
            if(datas['status']==1):
                for data in datas['matches']:
                    seqnum=data['match_seq_num']
                    x=json.dumps(data)+'\n'
                    fileJson.write(x)
            else:
                success=0
                break
            i+=1
        except BaseException:
            time.sleep(30)
    fileJson.close()


# for jsonIdex in range(1,1000,1):
#     fileJson = open(
#         "F:/dota2win/Dota2WinPrediction/Data/TrainData" + jsonIdex + ".JSON", "w")

# ma = api.get_match_history_by_seq_num(start_at_match_seq_num=seqnum)

# for i in ma['matches']:
#     x = json.dumps(i) + '\n'
#     fileJson.write(x)
