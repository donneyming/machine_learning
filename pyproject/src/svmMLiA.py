'''
Created on 2017-2-1

@author: cms
'''
from numpy import *
from time import sleep

def loadDataSet(filename):
    dataMat =[];labelMat =[]
    fr =open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat
def selectJrand(i,m):
    j =i
    while(j==i):
        j =int(random.uniform(0,m))
    return j
def clipAlpha(aj,H,L):
    if aj >H:
        aj = H
    if L > aj:
        aj = L
    return aj

def smosimple(dataMatIn,classLabels,C,toler,maxIter):
    dataMatrix = mat(dataMatIn);labelMat = mat(classLabels).transpose()
    b =0; m,n = shape(dataMatrix)
    alphas = mat(zeros((m,1)))
    iter = 0
    while(iter < maxIter):
        alpaParisChanged = 0
        for i in range(m):
            fXi = float(multiply(alphas,labelMat).T* (dataMatrix *dataMatrix[i,:].T))+b
            Ei = fXi -float(labelMat[i])
            if ((labelMat[i]*Ei <-toler) and (alphas[i]<C))or ((alphas[i] >0) and (labelMat[i]*Ei >toler)):
                j =selectJrand(i, m)
                fXj =float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T))+b
                Ej =fXj -float(labelMat[j])
                alphaIold = alphas[i].copy();
                alphaJold = alphas[j].copy();
                if (labelMat[i]!= labelMat[j]):
                    L =max(0,alphas[j]-alphas[i])
                    H =min(C,C+alphas[j]-alphas[i])
                else:
                    L =max(0,alphas[j]+alphas[i] -C)
                    H= min(C,alphas[j]+alphas[i])
                if L==H:print "L+H";continue
                eta =2.0*dataMatrix[i,:]*dataMatrix[j,:].T-dataMatrix[i,:]*dataMatrix[i,:].T-dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >=0:
                    print"ata>=0";continue
                alphas[j] -=labelMat[j]*(Ei-Ej)/eta
                alphas[j] =clipAlpha(alphas[j], H, L)
            if(abs(alphas[j] -alphaJold) <0.000001):print "j not moving enough";continue
            alphas[i] +=labelMat[j]*labelMat[i]*(alphaJold-alphas[j])
            b1 = b -Ei-labelMat[i]*(alphas[i]-alphaIold)*\
                dataMatrix[i,:]*dataMatrix[i,:].T-\
                labelMat[j]*(alphas[j]-alphaJold)*\
                dataMatrix[i,:]*dataMatrix[j,:].T
            b2 = b -Ej-labelMat[i]*(alphas[i]-alphaIold)*\
                dataMatrix[i,:]*dataMatrix[j,:].T-\
                labelMat[j]*(alphas[j]-alphaJold)*\
                dataMatrix[j,:]*dataMatrix[j,:].T
            if (0 <alphas[i]) and (C>alphas[i]):b = b1
            elif (0<alphas[j]) and (C>alphas[j]):b =b2
            else: b =(b1+b2)/2.0
            alpaParisChanged +=1
            print "iter:%d i:%d,pairs changed %d"%(iter,i,alpaParisChanged)
        if(alpaParisChanged == 0):iter +=1
        else:iter =0
        print "iter  numer:%d"%iter
    return b,alphas  

if __name__ == '__main__':
    dataArr,labelArr =loadDataSet('svmtest/testSet.txt')
    smosimple(dataArr,labelArr,0.6,0.001,40)