MyKey = "537AD5C3BDCBF53BAFCCA57D016C6514"#steam api keyupdata
China = [161, 163, 221, 222, 223, 224, 225, 231]
import time
import json
import dota2api
import os
import sys
api = dota2api.Initialise(api_key=MyKey,language='zh_CN')
def restart_program():
	print("restart!!")
	python = sys.executable
	os.execl(python, python, * sys.argv)

def collect():
    data1=open("F:/dota2win/Dota2WinPrediction/Data/data.txt","r")
    data1lines=data1.readlines()
    seqnum = int(data1lines[0])
    start=int(data1lines[1])+1
    data1.close()
    
    #ma=api.get_match_details(match_id=4324781398)
    success=1
    errCount=0
    for jsonnIdex in range(start,3001,1):
        if(success==0):
            break
        fileJson=open("F:/dota2win/Dota2WinPrediction/Data/RawData/TrainData" + str(jsonnIdex) + ".JSON", "w")
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
                errCount+=1
                print("出错%d次"%(errCount))
                if(errCount==5):
                    restart_program()
				# restart_program()
        fileJson.close()
        data1=open("F:/dota2win/Dota2WinPrediction/Data/data.txt","w")
        data1.write(str(seqnum)+'\n')
        data1.write(str(jsonnIdex))
        data1.close()
        print("当前进度:%.2f%%"%((jsonnIdex-1000)/20))
        
def CollectionByVHLevel():
    success=1
    for index in range(1,101):
        if(success==0):
            break
        fileJson=open("F:/dota2win/Dota2WinPrediction/Data/RawData/NewTrainData" + str(index) + ".JSON", "w")
        i=1
        while(i<10):
            try:
                datas=api.get_match_history(skill=3)
                if(datas["status"]==1):
                    for data in datas["matches"]:
                        x=json.dumps(data)+'\n'
                        fileJson.write(x)
                else:
                    success=0
                    break
                i+=1
            except BaseException:
                time.sleep(30)
        fileJson.close()
        print("当前进度:%.2f%%"%((index)/100))


if __name__ == '__main__':
    CollectionByVHLevel()
    # collect()
# for jsonIdex in range(1,1000,1):
#     fileJson = open(
#         "F:/dota2win/Dota2WinPrediction/Data/TrainData" + jsonIdex + ".JSON", "w")

# ma = api.get_match_history_by_seq_num(start_at_match_seq_num=seqnum)

# for i in ma['matches']:
#     x = json.dumps(i) + '\n'
#     fileJson.write(x)
