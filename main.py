import datetime
from functools import partial
from tkinter import *
from datetime import date, timedelta, datetime

global currentTime, resultOutput, ending, lastEventIndex, today, yesterday, firstSlash, secondSlash, dailyLogStreak
global commitStreak


root = Tk()
root.geometry("800x800")

dayOneOfDailyLogStreak = datetime(2021, 9, 26)
dayOneOfCommitStreak = datetime(2021, 11, 5)

resultOutput = ""
blankEndTime = False
currentLog = []
lastEventIndex = 0
firstTime = True
myScreen = []
myGrid = []

td = date.today()
yd = td - timedelta(days=1)
today = td.strftime("%m/%d/%Y")
yesterday = yd.strftime("%m/%d/%Y")

firstSlash = yesterday.find("/")
secondSlash = yesterday[firstSlash+1:].find("/") + firstSlash
firstSlashToday = today.find("/")
secondSlashToday = today[firstSlash+1:].find("/") + firstSlashToday

tdAsDateTime = datetime(int(today[-4:]), int(today[:firstSlashToday]), int(today[firstSlashToday+1:secondSlashToday+1]))
dailyLogStreak = (tdAsDateTime-dayOneOfDailyLogStreak).days
commitStreak = (tdAsDateTime-dayOneOfCommitStreak).days + 1

pastNumOfElem = 6


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
            output()


# Useful for copying the current log for external use, since you can't highlight and copy the label manually
def copyLog(firstLog):
    global resultOutput
    if not firstLog:
        lastTime = myScreen[0].get()
        resultOutput = "Access Daily Log - " + today +" http://wileyphillips.com/daily-log-" + yesterday[:2]
        resultOutput += "-" + yesterday[firstSlash+1:secondSlash+1] + "-" + yesterday[-4:] + "/\n"
        resultOutput += "Current Streak: Daily Log - " + str(dailyLogStreak) + ", Commit - " + str(commitStreak) + "\n"
        resultOutput += myScreen[-3-(pastNumOfElem-6)].get() + "\nToday's Goal: " + myScreen[-2-(pastNumOfElem-6)].get() + "\n"
        resultOutput += lastTime + ": " + myScreen[1].get() + "\n"
        for i in range(int(len(myScreen[2:pastNumOfElem*-1])/2)):
            newTime = myScreen[i * 2 + 2].get()
            activity = myScreen[i * 2 + 3].get()
            resultOutput += lastTime + " - " + str(newTime)+": " + str(activity) + "\n"
            lastTime = newTime
        resultOutput += "In Closing: " + myScreen[-1-(pastNumOfElem-6)].get()
    root.clipboard_clear()
    root.clipboard_append(resultOutput)


def addActivity():
    global lastEventIndex
    lastEventIndex += 1
    # Adds a new event entry along with an entry for time
    for i in range(2):
        myScreen.insert(-6-(pastNumOfElem-6), Entry(root))
        myScreen[-7-(pastNumOfElem-6)].grid(row=lastEventIndex, column=i)
    # Moves the bottom three buttons down one row
    myScreen[-6-(pastNumOfElem-6)].grid(row=lastEventIndex + 1, column=0),
    myScreen[-5-(pastNumOfElem-6)].grid(row=lastEventIndex + 1, column=1),
    myScreen[-4-(pastNumOfElem-6)].grid(row=lastEventIndex + 2, column=0)


def subtractActivity():
    global lastEventIndex
    if len(myScreen) > (2+pastNumOfElem):
        lastEventIndex -= 1
        # Adds a new event entry along with an entry for time
        for i in range(2):
            myScreen[-7-(pastNumOfElem-6)].destroy()
            myScreen.pop(-7-(pastNumOfElem-6))
        # Moves the bottom three buttons up one row
        myScreen[-6-(pastNumOfElem-6)].grid(row=lastEventIndex + 1, column=0),
        myScreen[-5-(pastNumOfElem-6)].grid(row=lastEventIndex + 1, column=1),
        myScreen[-4-(pastNumOfElem-6)].grid(row=lastEventIndex + 2, column=0)


def setScreen(isLeft):
    global myScreen, myGrid
    myScreen[0].destroy()
    myScreen[1].destroy()
    myScreen = []
    myGrid = []
    if isLeft:
        myScreen = [Label(root, text="Activity"),  # for current log
                    Entry(root),  # for current log
                    Button(root, command=partial(logCurrent, True), text="Start"),  # for current log
                    Button(root, command=partial(logCurrent, False), text="End"),  # for current log
                    Label(root, text="Press to Copy Log"),  # for current log
                    Button(root, command=partial(copyLog, True)),  # for current log
                    Label(root, text=""),  # for current log
                    ]
        setGrid(True)
    else:
        myScreen = [
            Entry(root),  # for past log
            Entry(root),  # for past log
            Button(root, command=addActivity, text="+"),  # for past log
            Button(root, command=subtractActivity, text="-"),  # for past log
            Button(root, command=partial(copyLog, False), text="Copy"),  # for past log
            Entry(root),  # for past log
            Entry(root),  # for past log
            Entry(root)  # for past log
            ]
        setGrid(False)



def setGrid(isLeft):
    global myScreen, firstTime, myGrid
    if isLeft:
        myGrid = [myScreen[0].grid(row=0, column=0),  # Label "Activity"
                  myScreen[1].grid(row=1, column=0),  # Entry for activity in progress
                  myScreen[2].grid(row=2, column=0),  # Button that starts activity
                  myScreen[3].grid(row=2, column=1),  # Button that ends activity
                  myScreen[4].grid(row=3, column=0),  # Label "Press to Copy Log"
                  myScreen[5].grid(row=3, column=1),  # Button that Copies the log made via live input
                  myScreen[6].grid(row=4, column=0),  # Label displays the live log
                  ]
    else:
        myGrid = [myScreen[0].grid(row=lastEventIndex, column=0),  # Entry for the time on past log
                  myScreen[1].grid(row=lastEventIndex, column=1),  # Entry for the activity on past log
                  myScreen[2].grid(row=lastEventIndex + 1, column=0),  # Button that adds a new activity
                  myScreen[3].grid(row=lastEventIndex + 1, column=1),  # Button that subtracts an activity
                  myScreen[4].grid(row=lastEventIndex + 2, column=0),  # Button that copies the past log
                  myScreen[5].grid(row=0, column=2),
                  myScreen[6].grid(row=1, column=2),
                  myScreen[7].grid(row=2, column=2)
                  ]


def pickLogType():
    global myScreen, myGrid
    myScreen = [Button(root, command=partial(setScreen, True), text="Current Log"),
                Button(root, command=partial(setScreen, False), text="Past Log")
                ]
    myGrid = [myScreen[0].grid(row=0, column=0),
              myScreen[1].grid(row=0, column=1)
              ]


pickLogType()

root.title("Daily Log Tool")

root.mainloop()
