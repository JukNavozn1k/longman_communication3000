from tkinter import *
from random import randint



# считываем слова
with open('data/words.txt','r')as w, open('data/translated.txt','r') as tw:
   
        words = w.read()
        words = words.split('\n')

        translated_words = tw.read()
        translated_words = translated_words.split('\n')
        
        print('Loaded words:  (RU {} ENG {})'.format(len(translated_words),len(words)))
 
# Подсчёт статистики
good = True
goodans = 0
badans = 0
sumary = 0
# считываем статистику, если таковая имеется
try:
    with open('data/stats.txt','r') as f:
        goodans,badans = map(int,f.readline().split())
        sumary = goodans + badans
except:
    print('Error! Stats file not found =(')
else: print('Stats loaded =)')
# следующее слово
def next_word():
    global wordlbl,words,root,idx,lang,translated_words,statuslbl,good
    good = True

    idx = randint(0,len(words)-1) 
    lang = randint(0,1) 

    if lang == 0: word = words[idx]
    else: word = translated_words[idx]

    wordlbl.config(text = " Word: {}".format(word))
    ansField.delete("1.0","end")
    translateBtn["state"] = DISABLED
    good = True
# перевод слова
def translate():
    global ansField,idx,words,translated_words,lang,good
    ansField.delete("1.0","end")
    good = False
    if lang == 0: ansField.insert(END,translated_words[idx])
    else: ansField.insert(END,words[idx])
# проверка ответа 
def answer():
    global idx,ansField,words,translated_words,lang,badans,goodans,good,sumary,statslbl
    word = ansField.get("1.0",END).lower()
    if lang == 1: 
        
        if  words[idx] in word:
            statuslbl.config(text='    status: OK')
            if good: goodans += 1
            next_word()
        else:
            statuslbl.config(text='    status: FAIL')
            translateBtn["state"] = NORMAL
            badans += 1
    else:
        if  translated_words[idx] in word:
            statuslbl.config(text='    status: OK')
            if good: goodans += 1
            next_word()
        else:
            statuslbl.config(text='    status: FAIL')
            translateBtn["state"] = NORMAL
            badans += 1
    sumary = goodans + badans

    statslbl.config(text='Correct ans: {} | Bad ans: {} | Summary: {}'.format(goodans,badans,goodans + badans))
    # в целях оптимизации разумнее записывать раз в несколько слов, но я записываю каждое слово (вроде тянет)
    if sumary % 1 == 0:
        with open('data/stats.txt','w') as f: f.write('{} {}'.format(goodans,badans))
            




# create root window
root = Tk()


# root window title and dimension
root.title("Longman Communication 3000 // v 0.3")
# Set geometry(widthxheight)
root.geometry('500x200')
root.resizable(False,False)
 
#adding a label to the root window
idx = randint(0,len(words)-1) # word idx from list
lang = randint(0,1) # 0 eng 1 ru 


if lang == 0: word = words[idx]
else: word = translated_words[idx]
wordlbl = Label(root, text = "Word: {}".format(word),font=('Times New Roman',14,'normal'))
wordlbl.grid(column=1,row=0)


# Следующее слово
nextBtn = Button(root, text = "Next" ,
             fg = "black", command=next_word,font=('Times New Roman',12,'normal'),width=7)
nextBtn.grid(column=0, row=1) 


translateBtn = Button(root, text = "Translate" ,
             fg = "black", command=translate,font=('Times New Roman',12,'normal'),width=7)
translateBtn.grid(column=0, row=3) 
translateBtn["state"] = DISABLED

ansBtn = Button(root, text = "Answer" ,
             fg = "black", command=answer,font=('Times New Roman',12,'normal'),width=7)
ansBtn.grid(column=0, row=2) 





# adding Text Field
ansField = Text(root, height=1,width=20,font=('Times New Roman',14,'normal'))


ansField.grid(column = 1, row =1)


statuslbl = Label(root, text = "    status: waiting... ".format(word),font=('Times New Roman',12,'normal'))
statuslbl.grid(column=1,row=3)


statslbl = Label(root, text = 'Correct ans: 0 | Bad ans: 0 | Summary: 0',font=('Times New Roman',12,'normal'))
statslbl.config(text='Correct ans: {} | Bad ans: {} | Summary: {}'.format(goodans,badans,goodans + badans))
statslbl.grid(column=1,row=2)



# Execute Tkinter
root.mainloop()
        
    