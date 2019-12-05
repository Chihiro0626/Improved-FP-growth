import TwoTableFPgrowth
import time



#simple data
start = time.time()
simDat = TwoTableFPgrowth.loadSimpDat()
initSet = TwoTableFPgrowth.createInitSet(simDat)
myFPtree, myHeaderTab ,myfreqItemSet , myCount_dict = TwoTableFPgrowth.createFPtree(initSet, 2)
print(myfreqItemSet)      #输出频繁项，从大到小
#myFPtree.disp()           #输出FP树
#myfreqItemSet_number,myDataFrame = TwoTableFPgrowth.dataframe(myfreqItemSet,myCount_dict)
#print(myfreqItemSet_number)     #dataframe中频繁项对应的序号
#print(myDataFrame)              #二维表
#mycalSuppDataDict = TwoTableFPgrowth.calSuppData(myDataFrame,myfreqItemSet_number)

#ImprovedFPgrowth.mineFPtree(myHeaderTab,myfreqItemSet,2,mycalSuppDataDict)
#freqSetSupp = []
#TwoTableFPgrowth.mineFPtree(myFPtree,myHeaderTab,2,set([]),freqSetSupp)
#print(freqSetSupp)
#TwoTableFPgrowth.freqSuppData(myHeaderTab,freqSetSupp,mycalSuppDataDict,2)

end = time.time()
print(end - start)

'''
#Random number data

start = time.time()
with open("D:\code\data\data1000.txt", "rb+") as f:
    parsedDat = [line.decode().split() for line in f.readlines()]
initSet = TwoTableFPgrowth.createInitSet(parsedDat)
myFPtree, myHeaderTab ,myfreqItemSet , myCount_dict = TwoTableFPgrowth.createFPtree(initSet, 200)
print(myfreqItemSet)      #输出频繁项，从大到小
#myFPtree.disp()           #输出FP树
#myfreqItemSet_number,myDataFrame = TwoTableFPgrowth.dataframe(myfreqItemSet,myCount_dict)
#print(myfreqItemSet_number)     #dataframe中频繁项对应的序号
#print(myDataFrame)              #二维表
#mycalSuppDataDict = TwoTableFPgrowth.calSuppData(myDataFrame,myfreqItemSet_number)

#ImprovedFPgrowth.mineFPtree(myHeaderTab,myfreqItemSet,2,mycalSuppDataDict)
#freqSetSupp = []
#TwoTableFPgrowth.mineFPtree(myFPtree,myHeaderTab,100000,set([]),freqSetSupp)
#print(freqSetSupp)
#TwoTableFPgrowth.freqSuppData(myHeaderTab,freqSetSupp,mycalSuppDataDict,100000)

end = time.time()
print(end - start)

'''