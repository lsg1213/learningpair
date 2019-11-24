from error import unexpectedError
from fileIO import fileIO, criticalQuestion
import random
from tkinter import *


def clear(window):
    for widget in window.winfo_children():
        widget.destroy()

def asking(qList, character, ch, window):
    criterion = 8   # 점수 기준
    ok = False  # criterion 이상의 점수를 받은 캐릭터가 있는지 여부
    m = ''   # criterion 이상의 점수를 받은 캐릭터 이름
    #ommand= lambda: action(someNumber)
    # 질문 리스트를 돌며 질문하고 대답을 저장
    # random.shuffle(qList)
    answer = IntVar()   
    for i in range(len(qList)):
        Q = Label(window, text=qList[i][0], font=('궁서체',20))
        Q.pack()
        
        yes = Radiobutton(window, text='맞다.', variable=answer, value=1, command=lambda : clear(window))
        no = Radiobutton(window, text='아니다.', variable=answer, value=0, command=lambda : clear(window))
        dontknow = Radiobutton(window, text='모른다.', variable=answer, value=-1, command=lambda : clear(window))
        yes.pack()
        no.pack()
        dontknow.pack()
        yes.wait_variable(answer)

        # answer 계산. answer가 1,2,3이므로 맞다, 아니다, 모른다를 1,-1,0으로 환산
        if answer.get() == 1 or answer.get() == 0:
            for j in range(0,len(character)):
                if answer.get() == qList[i][j + 2]:
                    character[j][1] += 1
                    if character[j][1] >= criterion:
                        ok = True
                        m = j
                else:
                    character[j][1] -= 1
                character[j][0][i] = answer.get()
        elif answer.get() == -1:
            continue
        else:
            raise unexpectedError('예기치 않은 오류 발생!')

        # 기준 점수 이상을 받은 캐릭터가 있고 동점이 없으면 출력, 동점이 있으면 계속 진행
        if ok:
            highestScore = []
            for j in range(len(character)):
                if character[m][1] == character[j][1]:
                    highestScore.append(j)  #해당 캐릭터의 인덱스
            if len(highestScore) == 1:
                window.geometry('1000x800')
                photo = PhotoImage(file="./image/"+ch[highestScore[0]]+".png")
                targetPhoto = Label(image=photo)
                targetPhoto.image = photo
                targetPhoto.pack()
                
                target = Label(window,text=ch[highestScore[0]], font=('궁서체',20))
                target.pack()
                var = IntVar()
                finish = Button(window,text="끝내기", width=5,height=5, command=lambda: var.set(1))
                finish.pack()
                finish.wait_variable(var)
                return True
            else:
                # critical 질문 시작
                criticalQ = criticalQuestion()
                tmp = list(highestScore)
                answer = IntVar()
                for k in tmp:
                    Q = Label(window, text=criticalQ[k][0], font=('궁서체',20))
                    Q.pack()
                    
                    yes = Radiobutton(window, text='맞다.', variable=answer, value=1, command=lambda : clear(window))
                    no = Radiobutton(window, text='아니다.', variable=answer, value=0, command=lambda : clear(window))
                    dontknow = Radiobutton(window, text='모른다.', variable=answer, value=-1, command=lambda : clear(window))
                    yes.pack()
                    no.pack()
                    dontknow.pack()
                    yes.wait_variable(answer)


                    if answer.get() == 1:
                        window.geometry('1000x800')
                        photo = PhotoImage(file="./image/"+ch[k]+".png")
                        targetPhoto = Label(image=photo)
                        targetPhoto.image = photo
                        targetPhoto.pack()
                        
                        target = Label(window,text=ch[k], font=('궁서체',20))
                        target.pack()
                        var = IntVar()
                        finish = Button(window,text="끝내기", width=5,height=5, command=lambda: var.set(1))
                        finish.pack()
                        finish.wait_variable(var)
                        return True
                    elif answer.get() == 0:
                        highestScore.remove(k)
                    else:
                        break
                if len(highestScore) == 0:
                    return asking(qList,character,ch,window)   # 만약 끝까지 정답 안 나오면 재시작
    return False

def akinator():
    # 위젯 전체 삭제 및 창사이즈 조절
    window.geometry('400x400')
    for widget in window.winfo_children():
        widget.pack_forget()

    qList = []  #[[질문,특징번호,질문개수,선택지1,선택지2,선택지3]]
    character = []  #[[특징번호가 index이고 수치가 value], 질문 총합 점수]
    # csv파일 접근하여 데이터 in
    fileIO(qList, character)

    ch = qList[0]
    ch = ch[2:]
    del qList[0]

    for i in range(len(qList)):
        for j in range(len(qList[i])):
            if qList[i][j].isdigit():
                qList[i][j] = int(qList[i][j])

    if(asking(qList, character, ch, window)):
        print('정상 종료')
        exit()
    else:
        for i in range(len(character)):
            character[i].append(i)
        sortedCharacter = sorted(character, key=lambda k : k[1], reverse=True)
        window.geometry('1000x800')
        photo = PhotoImage(file="./image/"+ch[sortedCharacter[0][2]]+".png")
        targetPhoto = Label(image=photo)
        targetPhoto.image = photo
        targetPhoto.pack()
        
        target = Label(window,text=ch[sortedCharacter[0][2]], font=('궁서체',20))
        target.pack()
        var = IntVar()
        finish = Button(window,text="끝내기", width=5,height=5, command=lambda: var.set(1))
        finish.pack()
        finish.wait_variable(var)
    


if __name__ == "__main__":
    window = Tk()
    window.geometry('1000x800')

    photo = PhotoImage(file="./image/akinator.png")
    genie = Label(image=photo)
    genie.image = photo
    genie.pack()

    start = Button(window, text='시작', command=akinator)
    start.config(height=5,width=20)
    start.pack()

    end = Button(window, text='종료', command=exit)
    end.config(height=5,width=20)
    end.pack()
    
    window.mainloop()
    
    
    