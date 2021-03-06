rawData = """
1 English Alex Network 1  20 High 2 non-English David Database 2 20 High 3 non-English David Programming 2 20 Medium 
4 non-English Bob Database 2 50 Low 5 non-English David Programming  2  30 High 6 non-English Alex Network 1 30 High
 7 non-English Alex Database  2 10 Low 8 non-English David Programming  2 20 Medium 9 non-English Alex Network  1 20 
 Medium 10 non-English Bob Algorithm 2  40 Medium 11 English Alex Network 2 40 Low 12 English David Database 1 10 Low 
 13 non-English Bob Programming 2 40 Medium 14 English Bob Algorithm 2 30 Medium 15 English David Algorithm  2 50 High
  16 non-English Bob Network 2 50 Medium 17 English Bob Database 1 50 High 18 non-English David Algorithm 1 10 Medium
   19 English Alex Network 2 30 Low  20 non-English Alex Programming 1 20 Medium
"""
attrName = ['#', 'Language', 'Instructor', 'Course', 'Semester', 'ClassSize', 'Score']

def reshape_list(rawData, newRowNum, newColNum):
    if rawData.__len__() != (newRowNum * newColNum):
        return None
    else:
        resultList = []
        for i in range(0, newRowNum):
            resultList.append(rawData[i*newColNum:i*newColNum+newColNum])
        return resultList

listedData = attrName
for e in rawData.split():
    listedData.append(e)

dataTable = reshape_list(listedData, newColNum=7, newRowNum=21)
