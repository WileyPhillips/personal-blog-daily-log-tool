import datetime
from functools import partial
from tkinter import *
from datetime import date, timedelta, datetime

root = Tk()
root.geometry("1920x1080")


dayOneOfDailyLogStreak = datetime(2021, 9, 26)
dayOneOfCommitStreak = datetime(2021, 11, 5)
streaks = [dayOneOfDailyLogStreak, dayOneOfCommitStreak]

resultOutput = ""
blankEndTime = False
currentLog = []
lastEventIndex = 0
firstTime = True


def date_change(up):
    global td, yesterday
    if up:
        td = td + timedelta(days=1)
    else:
        td = td - timedelta(days=1)
    yd = td - timedelta(days=1)
    today = td.strftime("%m/%d/%Y")
    yesterday = yd.strftime("%m/%d/%Y")

    firstSlash = yesterday.find("/")
    secondSlash = yesterday[firstSlash + 1:].find("/") + firstSlash
    firstSlashToday = today.find("/")
    secondSlashToday = today[firstSlash + 1:].find("/") + firstSlashToday

    tdAsDateTime = datetime(int(today[-4:]), int(today[:firstSlashToday]),
                            int(today[firstSlashToday + 1:secondSlashToday + 1]))
    dailyLogStreak = (tdAsDateTime - dayOneOfDailyLogStreak).days
    commitStreak = (tdAsDateTime - dayOneOfCommitStreak).days + 1

    myScreen[0][1].config(text=today)


shortHandDict = {
    "1": "Did some calisthenics.",
    "2": "Did some lifting.",
    "3": "Got ready.",
    "4": "Went and worked a shift.",
    "5": "Did some cardio.",
    "6": "Worked on daily log.",
    "7": "Updated food log.",
    "8": "Ate breakfast.",
    "9": "Ate lunch.",
    "10": "Ate Dinner.",
    "11": "Had a snack.",
    "12": "Went through night routine."
}


def set_screen():
    global myScreen, td, topElements, events
    events = []
    topElements = [
        Button(root, command=partial(date_change, False)),
        Label(root, text=""),
        Button(root, command=partial(date_change, True)),
        Label(root, text="Intro"),
        Entry(root),
        Label(root, text="Goal"),
        Entry(root),
        Label(root, text="Conclusion"),
        Entry(root),
        Label(root, text="Change Event Total"),
        Button(root, command=add_activity),
        Button(root, command=sub_activity)
    ]
    myScreen = [
        topElements,
        events
    ]
    set_grid()
    td = date.today()
    td = td - timedelta(days=1)
    date_change(True)


def set_grid():
    global myGrid, topElements
    myGrid = [
        topElements[0].grid(row=0, column=0),
        topElements[1].grid(row=0, column=1),
        topElements[2].grid(row=0, column=2),
        topElements[3].grid(row=0, column=3),
        topElements[4].grid(row=0, column=4),
        topElements[5].grid(row=0, column=5),
        topElements[6].grid(row=0, column=6),
        topElements[7].grid(row=0, column=7),
        topElements[8].grid(row=0, column=8),
        topElements[9].grid(row=0, column=9),
        topElements[10].grid(row=0, column=10),
        topElements[11].grid(row=0, column=11)
    ]


def add_activity():
    global events
    print(len(events))
    events.append(Entry(root))
    events[-1].grid(row=int(((len(events)-1)/2)+1), column=0)
    events.append(Entry(root))
    events[-1].grid(row=int(((len(events) - 2) / 2) + 1), column=1)
    print(len(events))

# ERROR doesn't remove from screen
def sub_activity():
    global events
    print(len(events))
    if len(events) > 0:
        for i in range(2):
            events[-1].destroy
            events.pop(-1)
    print(len(events))


root.title("Daily Log Tool")
set_screen()

root.mainloop()
