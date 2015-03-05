#!/bin/python2.7
#!/bin/python2
#!/bin/python

import numpy as np
import scipy.stats as stats
import sys

DataSetName='jesterfinal151cols.csv'

def ComputeSim(row1,row2):
    
    cter=1
    SameList1=[]
    SameList2=[]
    while cter!=len(row1):
        if row1[cter]!=99 and row2[cter]!=99:
            SameList1.append(row1[cter])
            SameList2.append(row2[cter])
        cter+=1
    result=stats.pearsonr(np.array(SameList1),np.array(SameList2))
    if np.isnan(result[0]):
        print 'covariance is zero!'
        return (0,0)
    return result

def TopMatch(Index,RatingMatrix,n=10):
    
    cter=0
    Ranking=[]
    while cter!=RatingMatrix.shape[0]:
        if cter!=Index:
            Ranking.append((cter,ComputeSim(RatingMatrix[Index][1:],RatingMatrix[cter][1:])[0]))
        cter+=1
    Ranking.sort(key=(lambda data:data[1]),reverse=True)
    return Ranking[:n]

def GetRecommendedJoke(Index,RatingMatrix,n=10):
    
    Similarities=[]
    cter=0
    while cter!=RatingMatrix.shape[0]:
        if cter!=Index:
            print 'computing similarity of user %s:' %(cter)
            Similarities.append(ComputeSim(RatingMatrix[Index][1:],RatingMatrix[cter][1:])[0])
            if np.isnan(Similarities[-1]):
                print 'compute %s similarity error! ' %(cter)
                exit()
        cter+=1
    colindex=1
    RecommendScores=[]
    
    while colindex!=RatingMatrix.shape[1]:
        
        SumofSimandRate=SumofSim=rowindex=0
        while rowindex!=RatingMatrix.shape[0]:
            if RatingMatrix[rowindex,colindex]!=99 and rowindex!=Index:
                SumofSim+=(Similarities[rowindex] if rowindex<Index else Similarities[rowindex-1])
                SumofSimandRate+=RatingMatrix[rowindex,colindex]*(Similarities[rowindex] if rowindex<Index else Similarities[rowindex-1])
            rowindex+=1
        print colindex,SumofSim
        
        if SumofSim!=0:
            RecommendScore=SumofSimandRate/SumofSim
            RecommendScores.append((colindex,RecommendScore))
        colindex+=1
    RecommendScores.sort(key=(lambda data:data[1]),reverse=True)
    return RecommendScores[:n]

if __name__=="__main__":
    if len(sys.argv)!=2:
        print 'usage: ./UserBasedRecommend.py <User ID>(0~50691)'
        exit()
    RatingMatrix=np.genfromtxt(DataSetName,delimiter=',',filling_values=99)
    UserID=sys.argv[1]
    print GetRecommendedJoke(int(UserID),RatingMatrix)
