import csv
def fileIO(qList, character):
    # csv 파일을 열어 질문 리스트를 뽑아오고 정리
    with open('generalQuestion.csv','r',newline='') as qFile:
        qReader = csv.reader(qFile, quotechar='-')
        for row in qReader:
            qList.append(row)

    # csv 파일을 열어 캐릭터 리스트를 뽑아오고 정리
    with open('characterList.csv','r',newline='') as qFile:
        qReader = csv.reader(qFile, quotechar='-')
        for row in qReader:
            character.append([[None]*len(qList),0])
        
    
def criticalQuestion():
    qList = []
    with open('criticalQuestion.csv','r',newline='') as qFile:
        qReader = csv.reader(qFile, quotechar='-')
        for row in qReader:
            qList.append(row)
        del qList[0]



    return qList
