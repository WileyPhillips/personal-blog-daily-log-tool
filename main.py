from functools import partial
from tkinter import *
from datetime import datetime

# TODO Take care of the edge case where in the length of current time and the start time don't match

root = Tk()
root.geometry("400x400")

currentLog = []
blankEndTime = False
resultOutput = ""


def startSequence():
    global currentTime, currentLog
    currentLog.append(currentTime + " - --:---m: " + myScreen[1].get() + "\n")
    output()


def output():
    global currentLog, resultOutput
    resultOutput = ""
    for i in range(len(currentLog)):
        resultOutput += currentLog[i] + "\n"
    myScreen[6].config(text=resultOutput)


def logCurrent(isStart):
    global currentLog, blankEndTime, currentTime
    time = datetime.now().strftime('%H:%M')
    if int(time[0:2]) > 12:
        currentTime = str(int(time[0:2])-12)+time[2:]+"pm"
    else:
        currentTime = time + "am"
    # Checks if currently there is a start time without an accompanying end time.
    if not blankEndTime:
        # Hit to start the next task with no other activity currently in progress.
        if isStart:
            blankEndTime = True
            startSequence()
            print("False Start")
        # If they hit end time without an activity currently in progress nothing will occur.
    else:
        # In the case that they start logging the next activity without ending the previous
        # Uses the current time as the end time for the previous, and as the starting time for the current activity
        if isStart:
            currentLog[-1] = currentLog[-1][:len(currentTime)+3] + currentTime + currentLog[-1][len(currentTime)*2+4:]
            startSequence()
            print("True Start")
        else:
            blankEndTime = False
            currentLog[-1] = currentLog[-1][:len(currentTime)+3] + currentTime + currentLog[-1][len(currentTime)*2+4:]
            print(currentLog)
            output()
            print("True End")


# Useful for copying the current log for external use, since you can't highlight and copy the label manually
def copyLog():
    global resultOutput
    root.clipboard_clear()
    root.clipboard_append(resultOutput)


root.title("Daily Log Tool")
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
