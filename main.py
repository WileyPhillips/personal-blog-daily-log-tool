from functools import partial
from tkinter import *
from datetime import datetime


global currentTime, resultOutput, ending, lastEventIndex

root = Tk()
root.geometry("800x800")

resultOutput = ""
blankEndTime = False
currentLog = []
lastEventIndex = 0
firstTime = True
myScreen = []
myGrid = []


# Starts tracking an activity with an unspecified end time.
def startSequence():
    global currentTime, currentLog
    currentLog.append(currentTime + " - --:---m: " + myScreen[1].get() + "\n")
    output()


def output():
    global currentLog, resultOutput
    resultOutput = ""
    # each string in the list is to be on a separate line.
    for i in range(len(currentLog)):
        resultOutput += currentLog[i] + "\n"
    myScreen[6].config(text=resultOutput)


def formatTime():
    global currentTime, ending
    time = datetime.now().strftime('%H:%M')
    if int(time[0:2]) > 12:
        ending = "pm"
        currentTime = str(int(time[0:2]) - 12) + time[2:] + ending
    else:
        ending = "am"
        currentTime = time + ending


def logCurrent(isStart):
    global currentLog, blankEndTime, currentTime
    formatTime()
    # Checks if currently there is a start time without an accompanying end time.
    if not blankEndTime:
        # Hit to start the next task with no other activity currently in progress.
        if isStart:
            blankEndTime = True
            startSequence()
        # If they hit end time without an activity currently in progress nothing will occur.
    else:
        # In the case that they start logging the next activity without ending the previous
        # Uses the current time as the end time for the previous, and as the starting time for the current activity
        if isStart:
            currentLog[-1] = currentLog[-1][:currentTime.find(ending)+5] + currentTime + currentLog[-1][(currentTime.find(ending)+2)*2+3:]
            startSequence()
        # Replaces the end time's placeholder dashes with the current time
        else:
            blankEndTime = False
            currentLog[-1] = currentLog[-1][:len(currentTime)+3] + currentTime + currentLog[-1][len(currentTime)*2+3:]
            print(currentLog)
            output()
            print("True End")


# Useful for copying the current log for external use, since you can't highlight and copy the label manually
def copyLog(firstLog):
    global resultOutput
    root.clipboard_clear()
    root.clipboard_append(resultOutput)


def addActivity():
    global lastEventIndex
    lastEventIndex += 1
    # Adds a new event entry along with an entry for time
    for i in range(2):
        myScreen.insert(-3, Entry(root))
        myScreen[-4].grid(row=lastEventIndex, column=i+2)
    # Moves the bottom three buttons down one row
    myScreen[-3].grid(row=lastEventIndex + 1, column=2),
    myScreen[-2].grid(row=lastEventIndex + 1, column=3),
    myScreen[-1].grid(row=lastEventIndex + 2, column=2)




def subtractActivity():
    global lastEventIndex
    if len(myScreen) > 12:
        lastEventIndex -= 1
        # Adds a new event entry along with an entry for time
        for i in range(2):
            myScreen[-4].destroy()
            myScreen.pop(-4)
        # Moves the bottom three buttons up one row
        myScreen[-3].grid(row=lastEventIndex + 1, column=2),
        myScreen[-2].grid(row=lastEventIndex + 1, column=3),
        myScreen[-1].grid(row=lastEventIndex + 2, column=2)


def setScreen():
    global myScreen
    if firstTime:
        myScreen = [Label(root, text="Activity"),
                    Entry(root),
                    Button(root, command=partial(logCurrent, True), text="Start"),
                    Button(root, command=partial(logCurrent, False), text="End"),
                    Label(root, text="Press to Copy Log"),
                    Button(root, command=partial(copyLog, True)),
                    Label(root, text=""),
                    Entry(root),
                    Entry(root),
                    Button(root, command=addActivity, text="+"),
                    Button(root, command=subtractActivity, text="-"),
                    Button(root, command=partial(copyLog, False), text="Copy")
                    ]
    setGrid()


def setGrid():
    global myScreen, firstTime
    if firstTime:
        myGrid = [myScreen[0].grid(row=0, column=0),
                  myScreen[1].grid(row=1, column=0),
                  myScreen[2].grid(row=2, column=0),
                  myScreen[3].grid(row=2, column=1),
                  myScreen[4].grid(row=3, column=0),
                  myScreen[5].grid(row=3, column=1),
                  myScreen[6].grid(row=4, column=0),
                  myScreen[7].grid(row=lastEventIndex, column=2),
                  myScreen[8].grid(row=lastEventIndex, column=3),
                  myScreen[9].grid(row=lastEventIndex + 1, column=2),
                  myScreen[10].grid(row=lastEventIndex + 1, column=3),
                  myScreen[11].grid(row=lastEventIndex + 2, column=2)
                  ]
        firstTime = False


setScreen()

root.title("Daily Log Tool")

root.mainloop()
