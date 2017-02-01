'''
Created on 2017-2-1

@author: cms
'''
from numpy import  * 
def createVocabList(dataSet):
    vocabSet =set([])
    for document in dataSet:
        vocabSet =vocabSet|set(document)
    return list(vocabSet)

def setofWords2Vec(vocabList,inputSet):
    returnVec =[0]*len(vocabList)
    for word in vocabList:
        if word in vocabList:
            returnVec[vocabList.index(word)] =1
        else:
            print "the word :%s is not in Vocabulary!"%word
    return returnVec
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive =sum(trainCategory)/float(numTrainDocs)
    p0Num =zeros(numWords);p1Num=zeros(numWords)
    p0Denom =0.0;p1Denom= 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] ==1:
            p1Num += trainMatrix[i]
            p1Denom +=sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = p1Num/p1Denom
    p0Vect =p0Num/p0Denom
    return p0Vect,p1Vect,pAbusive
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1 = sum(vec2Classify*p1Vec)+log(pClass1)
    p0 = sum(vec2Classify*p0Vec)+log(1.0-pClass1)
    if p1>p0:
        return 1
    else:
        return 0

def bagOfWOrds2VecMN(vocabList,inputSet):
    returnVect =[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVect[vocabList.index(word)] +=1
    return returnVect

def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) >2]

def  spamTest():
    docList =[];classList=[];fullText=[]
    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50);testSet=[]
    for i in range(10):
        randIndex = int (random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(setofWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = setofWords2Vec(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!= classList[docIndex]:
            errorCount +=1
    print 'the error rate is ',float(errorCount)/len(testSet)
if __name__ == '__main__':
    spamTest()