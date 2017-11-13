from dataSet import dataTable

trainingData = dataTable[1:15]
testData = dataTable[15:21]


def compute_distance(record):
    attributeNumbre = record.__len__()
    distanceDict = {}
    for trainingRecord in trainingData:
        distance = 0
        for i in range(1, attributeNumbre - 1):
            if record[i] != trainingRecord[i]:
                distance += 1
        distanceDict[trainingRecord[0]] = distance
    return distanceDict

for record in testData:
    distance = compute_distance(record)
    distance = sorted(distance.items(), key=lambda x: int(x[0]), reverse=False)
    distance = sorted(distance, key=lambda x: x[1], reverse=False)
    print(record[0], distance, '\n')
