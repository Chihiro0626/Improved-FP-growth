# coding:utf-8
import itertools
import pandas as pd


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print('  ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)


def updateHeader(nodeToTest, targetNode):
    while nodeToTest.nodeLink != None:
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


#更新FP树
def updateFPtree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        # 判断items的第一个结点是否已作为子结点
        inTree.children[items[0]].inc(count)
    else:
        # 创建新的分支
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    # 递归
    if len(items) > 1:
        updateFPtree(items[1::], inTree.children[items[0]], headerTable, count)


#构造FP树
def createFPtree(dataSet, minSup=1):
    #频繁项
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable.keys()):
        if headerTable[k] < minSup:
            del (headerTable[k])  # 删除不满足最小支持度的元素
    #print(headerTable)
    freqItemSet_count = sorted(headerTable.items(), key=lambda p: (p[1], -ord(p[0])), reverse=True)  # 频繁项先按频繁度排序，再按字母排序
    print(freqItemSet_count)
    freqItemSet = [i[0] for i in freqItemSet_count]  # 频繁项
    if len(freqItemSet) == 0:
        return None, None, None , None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # element: [count, node]


    #FP树
    retTree = treeNode('Null Set', 1, None)
    freqDataSet = []  # 去除非频繁项的事务数据集列表
    for tranSet, count in dataSet.items():
        # dataSet：[element, count]
        localD = {}
        for item in tranSet:
            if item in freqItemSet:  # 过滤，只取该样本中满足最小支持度的频繁项
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            # 根据全局频数从大到小对单样本排序
            orderedItem = [v[0] for v in sorted(localD.items(), key=lambda p:(p[1], -ord(p[0])), reverse=True)]
            #orderedItem = [v[0] for v in sorted(localD.items(), key=lambda p:(p[1],int(p[0])), reverse=True)]
            # 用过滤且排序后的样本更新树
            freqDataSet.append(orderedItem)
            updateFPtree(orderedItem, retTree, headerTable, count)

    #频繁二项集
    freqItemTwo = list(itertools.combinations(freqItemSet, 2))
    count_dict = dict()  # 频繁二项集及其对应的频繁计数
    for item in freqItemTwo:
        count_dict[tuple(item)] = 0
        for trans in freqDataSet:
            if set(item) <= set(trans):
                count_dict[tuple(item)] += 1

    return retTree, headerTable , freqItemSet , count_dict




#创建二维列表
def dataframe(freqItemSet,count_dict):
    l = len(freqItemSet)
    freqItemSet_number = dict(zip(list(range(l)),freqItemSet))       #序号对应的字母字典集
    df = pd.DataFrame([[0 for _ in range(l)] for _ in range(l)],index=freqItemSet,columns=freqItemSet) #初始化二维列表，索引为频繁项，数据全为0
    #df = pd.DataFrame(np.zeros(shape=(l,l)),index=freqItemSet,columns=[list(range(l)),freqItemSet])
    #df = df.reset_index()
    for key , value in count_dict.items():
        df.ix[[key[0]],key[1]] = value
    return freqItemSet_number,df



#回溯
def ascendFPtree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendFPtree(leafNode.parent, prefixPath)


# 条件模式基
def findPrefixPath(basePat, myHeaderTab):
    treeNode = myHeaderTab[basePat][1]  # basePat在FP树中的第一个结点
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendFPtree(treeNode, prefixPath)  # prefixPath是倒过来的，从treeNode开始到根
        if len(prefixPath) > 1:
            condPats[tuple(prefixPath[1:])] = treeNode.count  # 关联treeNode的计数
        treeNode = treeNode.nodeLink  # 下一个basePat结点
    return condPats



#条件FP树
def mineFPtree(inTree,headerTable, minSup,preFix,freqSetSupp):
    # 最开始的频繁项集是headerTable中的各元素
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]  # 根据频繁项的总频次排序，默认从小到大
    for basePat in bigL:  # 对每个频繁项
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        condPattBases = findPrefixPath(basePat, headerTable)  # 当前频繁项集的条件模式基
        myCondTree , myHead , myFreq , myCount_dict = createFPtree(condPattBases, minSup)  # 构造当前频繁项的条件FP树
        if myHead != None:
            for item in condPattBases:
                if len(item) != 1:
                    #print('conditional tree for: ', basePat, newFreqSet, condPattBases)
                    #myCondTree.disp(1)
                    freqItemSet_number, df = dataframe(myFreq, myCount_dict)
                    #print(df)
                    myCalSuppDataDict = calSuppData(df, freqItemSet_number)
                    #print(myCalSuppDataDict)
                    freqSet = dict()
                    for k1, v1 in myCalSuppDataDict.items():
                        for k2, v2 in v1.items():
                            preNode = list(newFreqSet) + [k1, k2]
                            freqSet[tuple(preNode)] = v1[k2]
                    #print(freqSet)
                    freqSetSupp.append(freqSet)

                    mineFPtree(myCondTree, myHead, minSup, newFreqSet,freqSetSupp)  # 递归挖掘条件FP树    #如果此树不是单一路径，就需要递归挖掘条件FP树




#数据集
def loadSimpDat():
    simDat = [['A','B','C','E','F','O'],
              ['A','C','G'],['E','I'],
              ['A','C','D','E','G'],
              ['A','C','E','G','L'],
              ['E','J'],
              ['A','B','C','E','F','P'],
              ['A','C','D'],
              ['A','C','E','G','M'],
              ['A','C','E','G','N']]
    return simDat


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        key = frozenset(trans)
        if retDict.__contains__(key):
            retDict[frozenset(trans)] += 1
        else:
            retDict[frozenset(trans)] = 1
    return retDict



#利用dataframe进行支持度计数统计
def calSuppData(df,freqItemSet_number):
    calSuppDataDict = dict()
    for freq in freqItemSet_number:
        Colrow = dict(df.iloc[:,freq])
        Colrow = {key:value for key,value in Colrow.items() if value != 0}
        if Colrow != {}:
            calSuppDataDict[freqItemSet_number[freq]] = Colrow
    return calSuppDataDict




def freqSuppData(headerTable,freqSetSupp,calSuppDataDict,minSup):
    freqSetTwo = dict()  # 频繁二项集的集合
    for k, v in calSuppDataDict.items():
        freqItemtwo = []
        for item in v.keys():
            freqItemtwo.append(tuple([item, k]))
        freqItemtwoDict = dict(zip(freqItemtwo, v.values()))
        freqSetTwo.update(freqItemtwoDict)
    for k in list(freqSetTwo.keys()):
        if freqSetTwo[k] < minSup:
            del (freqSetTwo[k])

    freqSetOne = dict()
    for k,v in headerTable.items():
        freqSetOne[k] = v[0]

    freqSetSupp.append(freqSetTwo)
    freqSetSupp.append(freqSetOne)
    print(freqSetSupp)

