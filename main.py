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
myScreen = []
myGrid = []


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
    global myScreen, td
    topElements = [
        Button(root),
        Label(root, text="")
    ]
    events = []
    myScreen = [
        topElements,
        events
    ]
    set_grid()
    td = date.today()
    td = td - timedelta(days=1)
    date_change()


def set_grid():
    print("placeholder")

root.title("Daily Log Tool")

root.mainloop()
