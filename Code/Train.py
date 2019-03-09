import sklearn
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split,cross_val_score,StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier 
import json

def saveModel(model,filepath):
    sklearn.externals.joblib.dump(model,filename=filepath)

def loadModel(filepath):
    model=sklearn.externals.joblib.load(filepath)
    return model

def trainModel():
    dataset=pd.read_csv(u"F:/dota2win/Dota2WinPrediction/Data/AnalysisData/newdataset.csv")
    print(dataset.shape)
    y=dataset["天辉赢"]
    listX=[x for x in range(1,dataset.shape[1])]
    X=dataset.iloc[:,listX]
    # X_train, X_test, y_train, y_test = train_test_split(X,y)
    lr=LogisticRegression()
    # lr.fit(X_train,y_train)
    rf=RandomForestClassifier(max_depth=18)
    strKFold = StratifiedKFold(n_splits=10,shuffle=True)
    # rf.fit(X_train,y_train)
    kNN=KNeighborsClassifier(n_neighbors=8)
    # kNN.fit(X_train,y_train)
    # SVM=SVC()
    scoresLR=cross_val_score(lr,X,y,cv=strKFold,scoring='precision')
    scoresRF=cross_val_score(rf,X,y,cv=strKFold,scoring='precision')
    # scoresSVM=cross_val_score(SVM,X,y,cv=2)
    scoresKNN=cross_val_score(kNN,X,y,cv=3)
    print("逻辑回归")
    print(scoresLR)
    print("随机森林")
    print(scoresRF)
    # print("SVM")
    # print(scoresSVM)
    print("kNN")
    print(scoresKNN)
    # y_predictLR=lr.predict(X_test)
    # y_predictRF=rf.predict(X_train)
    # y_predictSVM=SVM.predict(X_test)
    # y_predictKNN=kNN.predict(X_test)
    # print("逻辑回归")
    # print(accuracy_score(y_test,y_predictLR))
    # print("随机森林")
    # print(accuracy_score(y_train,y_predictRF))
    # print("SVM")
    # print(accuracy_score(y_test,y_predictSVM))
    # print("KNN")
    # print(accuracy_score(y_train,y_predictKNN))

def trainLR():
    LRData=open("./Data/AnalysisData/LRData.json",'a')
    lr=LogisticRegression()
    scoresLR=cross_val_score(lr,X,y,cv=strKFold,scoring='precision')
    print("逻辑回归")
    print(scoresLR)
    dictLR={}
    for i in range(0,len(scoresLR)):
        # LRData.write(str(scoresLR[i])+',')
        dictLR[i]=scoresLR[i]
    LRData.write(json.dumps(dictLR))
    LRData.write('\n')
    LRData.close()

def trainRF():
    RFData=open("./Data/AnalysisData/RFData.json",'a')
    rf=RandomForestClassifier(max_depth=18)
    scoresRF=cross_val_score(rf,X,y,cv=strKFold,scoring='precision')
    print("随机森林")
    print(scoresRF)
    dictRF={}
    for i in range(0,len(scoresRF)):
        dictRF[i]=scoresRF[i]
    RFData.write(json.dumps(dictRF))
    RFData.write('\n')
    RFData.close()

def trainSVM():
    SVMData=open("./Data/AnalysisData/SVMData.json",'a')
    SVM=SVC()
    scoresSVM=cross_val_score(SVM,X,y,cv=strKFold,scoring='precision')
    print("SVM")
    print(scoresSVM)
    dictSVM={}
    for i in range(0,len(scoresSVM)):
        dictSVM[i]=scoresSVM[i]
    SVMData.write(json.dumps(dictSVM))
    SVMData.write('\n')
    SVMData.close()

def trainkNN(k=3):
    kNNData=open("./Data/AnalysisData/kNNData.json",'a')
    kNN=KNeighborsClassifier(n_neighbors=k)
    scoresKNN=cross_val_score(kNN,X,y,cv=strKFold,scoring='precision')
    print('kNN')
    print(scoresKNN)
    dictKNN={}
    for i in range(0,len(scoresKNN)):
        dictKNN[i]=scoresKNN[i]
    kNNData.write(json.dumps(dictKNN))
    kNNData.write('\n')
    kNNData.close()

def findBestCInLR():
    LRData=open("./Data/AnalysisData/LRNorm.json",'w')
    dictNorm={}
    vecC=[0.5*x for x in range(1,41)]
    for i in vecC:
        lr=LogisticRegression(C=i)
        lr.fit(X,y)
        scoresLR=cross_val_score(lr,X,y,cv=strKFold,scoring='precision')
        Accuracy=round(np.sum(scoresLR)/len(scoresLR),5)
        y_predictLR=lr.predict(X)
        AccuracyInTrain=round(accuracy_score(y,y_predictLR),5)
        vecRes=[Accuracy,AccuracyInTrain]
        dictNorm[i]=vecRes
    LRData.write(json.dumps(dictNorm,indent=4))
    LRData.close()

def findBestDepthInRF():
    RFData=open("./Data/AnalysisData/RFDepth.json",'a')
    dictDepth={}
    vecDepth=[x for x in range(5,31)]
    vecDepth.append(10000)
    for i in vecDepth:
        rf=RandomForestClassifier(max_depth=i)
        rf.fit(X,y)
        scoresRF=cross_val_score(rf,X,y,cv=strKFold,scoring='precision')
        Accuracy=round(np.sum(scoresRF)/len(scoresRF),5)
        y_predict=rf.predict(X)
        AccuracyInTrain=round(accuracy_score(y,y_predict),5)
        vecRes=[Accuracy,AccuracyInTrain]
        dictDepth[i]=vecRes
    RFData.write(json.dumps(dictDepth,indent=4))
    RFData.close()

if __name__ == '__main__':
    # trainModel()
    dataset=pd.read_csv(u"F:/dota2win/Dota2WinPrediction/Data/AnalysisData/newdataset.csv")
    y=dataset["天辉赢"]
    listX=[x for x in range(1,dataset.shape[1])]
    X=dataset.iloc[:,listX]
    strKFold = StratifiedKFold(n_splits=10,shuffle=True)
    # for i in range(1,11):
    #     trainLR()
    # for i in range(1,11):
    #     trainRF()
    # for i in range(3,9):
    #     trainkNN(k=i)
    # trainSVM()
    # findBestCInLR()
    findBestDepthInRF()
