Y = [-1, 1, 1, 1, -1, -1, 1, -1]


def calaulate_accuracy(c):
    if c.__len__() != Y.__len__():
        return -1
    errorCounter = 0
    for i in range(Y.__len__()):
        if c[i] != Y[i]:
            errorCounter += 1
    return float(errorCounter) / float(Y.__len__())


h1 = [-1, -1, 1, 1, 1, 1, 1, -1]
h2 = [-1, 1, 1, -1, 1, 1, -1, -1]
h3 = [1, 1, 1, 1, 1, 1, 1, 1]

print(calaulate_accuracy(h1))
print(calaulate_accuracy(h2))
print(calaulate_accuracy(h3))
