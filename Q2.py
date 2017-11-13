import numpy as np
import math
from dataSet import dataTable

attrName = [e[1:-1] for e in dataTable][0]
feature = [e[1:-1] for e in dataTable][1:]
target = [e[-1] for e in dataTable][1:]

global candidateList
candidateList = []
global nodeID
nodeID = 0

mode = 'ID3'  # 'ID3'
mode = 'C45'  # 'C4.5'

# (node, childList)
# each node -> (nodeID, [h, m, l])
nodeList = []


def get_node_detail(targetValue):
    nodeDetail = [0, 0, 0]
    for element in targetValue:
        if element == 'High':
            nodeDetail[0] += 1
        if element == 'Medium':
            nodeDetail[1] += 1
        if element == 'Low':
            nodeDetail[2] += 1
    return nodeDetail


def get_entropy(valueList):
    valueList = [float(e) for e in valueList]
    valueList = np.array(valueList)
    valueList = valueList / np.sum(valueList)
    entropy = 0
    for value in valueList:
        if value == 0:
            continue
        entropy = entropy + (-1) * value * math.log(value, math.e)
    return entropy


# data(feature, target, attrName, nodeID)
def split_once(data):
    global nodeID
    dataFeature = data[0]
    dataTarget = data[1]
    dataAttrName = data[2]
    myNodeID = data[3]
    attrNumber = dataFeature[0].__len__()
    itemNumber = dataFeature.__len__()
    # put current node into list
    nodeDetail = get_node_detail(dataTarget)
    parentEntropy = get_entropy(nodeDetail)
    parentNode = (myNodeID, nodeDetail, parentEntropy)

    # check leaf node
    targetCheckList = []
    for value in dataTarget:
        if value not in targetCheckList:
            targetCheckList.append(value)
    if targetCheckList.__len__() == 1:
        nodeList.append((parentNode, []))
        return 0

    # choose attr to split
    attrEntropy = []
    for i in range(attrNumber):
        entropy = 0
        # compute entropy for each attr
        attrCol = [e[i] for e in dataFeature]
        # key of attrCount is attr name, value is attr numbers
        attrCount = {}
        attrCountSum = 0
        # key of attrTarget is attr name, value is target numbers
        attrTarget = {}
        for i in range(itemNumber):
            attrValue = attrCol[i]
            if attrValue not in attrCount:
                attrCount[attrValue] = 0
            attrCount[attrValue] += 1
            if attrValue not in attrTarget:
                attrTarget[attrValue] = {}
            targetValue = dataTarget[i]
            if targetValue not in attrTarget[attrValue]:
                attrTarget[attrValue][targetValue] = 0
            attrTarget[attrValue][targetValue] += 1
        for value in attrCount:
            attrCountSum += attrCount[value]
        for attr in attrTarget:
            entropy = entropy + float(attrCount[attr]) * get_entropy([e[1] for e in attrTarget[attr].items()]) / float(attrCountSum)
        if mode == 'ID3':
            infoGain = parentEntropy - entropy
        if mode == 'C45':
            tmpEntropy = get_entropy([e[1] for e in attrCount.items()])
            if tmpEntropy == 0:
                infoGain = 0
            else:
                infoGain = (parentEntropy - entropy) / get_entropy([e[1] for e in attrCount.items()])
        attrEntropy.append((infoGain, attrCount, attrTarget))
    # value, position
    maxInfoGain = [-1, -1]
    for i in range(attrEntropy.__len__()):
        infoGain = attrEntropy[i][0]
        if infoGain > maxInfoGain[0] or maxInfoGain[0] == -1:
            maxInfoGain[0] = infoGain
            maxInfoGain[1] = i
    splitAttrCount = attrEntropy[maxInfoGain[1]][1]
    splitAttrTarget = attrEntropy[maxInfoGain[1]][2]
    childList = []
    for attr in splitAttrCount:
        try:
            h = splitAttrTarget[attr]['High']
        except:
            h = 0
        try:
            m = splitAttrTarget[attr]['Medium']
        except:
            m = 0
        try:
            l = splitAttrTarget[attr]['Low']
        except:
            l = 0
        nodeID += 1
        childList.append((nodeID, '%s=%s' % (dataAttrName[maxInfoGain[1]], attr), [h, m, l]))
        newFeature = []
        newTarget = []
        newAttrName = []
        for i in range(itemNumber):
            record = dataFeature[i]
            if record[maxInfoGain[1]] == attr:
                newFeature.append([record[i] for i in range(record.__len__()) if i != maxInfoGain[1]])
                newTarget.append(dataTarget[i])
        for i in range(dataAttrName.__len__()):
            if i != maxInfoGain[1]:
                newAttrName.append(dataAttrName[i])
        candidateList.append((newFeature, newTarget, newAttrName, nodeID))
    nodeList.append((parentNode, childList))
    pass

if __name__ == '__main__':
    # feature, target, attrName, nodeID
    candidateList.append((feature, target, attrName, 0))
    while candidateList.__len__() > 0:
        record = candidateList[0]
        del candidateList[0]
        split_once(record)
    for e in nodeList:
        print(e)
    nodeWriteList = []
    relationWriteList = []
    with open('Assignment_q2_%s.gv' % mode, 'w') as f:
        f.write('digraph Tree {\n')
        f.write('node [shape=box];\n')
        for record in nodeList:
            currentNode = record[0]
            if currentNode[0] not in nodeWriteList:
                f.write('%s [label="High=%s\\nMedium=%s\\nLow=%s"]\n' % (currentNode[0], currentNode[1][0],
                                                                       currentNode[1][1], currentNode[1][2]))
                nodeWriteList.append(currentNode[0])
            for childNode in record[1]:
                if childNode[0] not in nodeWriteList:
                    f.write('%s [label="%s\\nHigh=%s\\nMedium=%s\\nLow=%s"]\n' % (childNode[0], childNode[1],
                                                                                childNode[2][0], childNode[2][1],
                                                                                childNode[2][2]))
                    nodeWriteList.append(childNode[0])
                f.write('%s -> %s;\n' % (currentNode[0], childNode[0]))
        f.write('}')

