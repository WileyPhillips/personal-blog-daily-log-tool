from functools import partial
from tkinter import *
from datetime import datetime


root = Tk()
root.geometry("400x400")

currentLog = ""
lastAddition = ""
blankEndTime = False


def startSequence():
    global currentTime, currentLog, lastAddition
    lastAddition = currentTime + " - --:---m: " + myScreen[1].get() + "\n"
    currentLog += lastAddition
    myScreen[6].config(text=currentLog)


def logCurrent(isStart):
    global currentLog, lastAddition, blankEndTime, currentTime
    time = datetime.now().strftime('%H:%M')
    if int(time[0:2]) > 12:
        currentTime = str(int(time[0:2])-12)+time[2:]+"pm"
    else:
        currentTime = time + "am"
    if not blankEndTime:
        if isStart:
            blankEndTime = True
            startSequence()
            print("False Start")
    else:
        if isStart:
            currentLog = currentLog[:10-len(lastAddition)] + currentTime[:-1] + currentLog[16-len(lastAddition):]
            myScreen[6].config(text=currentLog)
            startSequence()
            print("True Start")
        else:
            blankEndTime = False
            currentLog = currentLog[:10 - len(lastAddition)] + currentTime[:-1] + currentLog[16 - len(lastAddition):]
            print(currentLog)
            lastAddition = ""
            myScreen[6].config(text=currentLog)
            print("True End")


def copyLog():
    global currentLog
    root.clipboard_clear()
    root.clipboard_append(currentLog)


root.title("Title")
myScreen = [Label(root, text="Test"),
            Entry(root),
            Button(root, command=partial(logCurrent, True), text="Start"),
            Button(root, command=partial(logCurrent, False), text="End"),
            Label(root, text="Press to Copy Log"),
            Button(root, command=copyLog),
            Label(root, text="")
            ]
myGrid = [myScreen[0].grid(row=0, column=0),
          myScreen[1].grid(row=1, column=0),
          myScreen[2].grid(row=2, column=0),
          myScreen[3].grid(row=2, column=1),
          myScreen[4].grid(row=3, column=0),
          myScreen[5].grid(row=3, column=1),
          myScreen[6].grid(row=4, column=0)
          ]

root.mainloop()
