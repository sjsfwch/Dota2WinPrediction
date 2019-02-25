import sklearn
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def saveModel(model,filepath):
    sklearn.externals.joblib.dump(model,filename=filepath)

def loadModel(filepath):
    model=sklearn.externals.joblib.load(filepath)
    return model

def trainModel():
    dataset=pd.read_csv(u"F:/dota2win/Dota2WinPrediction/Data/AnalysisData/dataset.csv")
    print(dataset.shape)
    y=dataset["天辉赢"]
    listX=[x for x in range(1,dataset.shape[1])]
    X=dataset.iloc[:,listX]
    X_train, X_test, y_train, y_test = train_test_split(X,y)
    lr=LogisticRegression()
    lr.fit(X_train,y_train)
    scores=cross_val_score(lr,X_train,y_train,cv=5)
    print(scores)
    y_predict=lr.predict(X_test)
    print(accuracy_score(y_test,y_predict))


if __name__ == '__main__':
    trainModel()