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

    first_slash = yesterday.find("/")
    second_slash = yesterday[first_slash + 1:].find("/") + first_slash
    first_slash_today = today.find("/")
    second_slash_today = today[first_slash + 1:].find("/") + first_slash_today

    td_as_date_time = datetime(int(today[-4:]), int(today[:first_slash_today]),
                               int(today[first_slash_today + 1:second_slash_today + 1]))
    daily_log_streak = (td_as_date_time - dayOneOfDailyLogStreak).days
    commit_streak = (td_as_date_time - dayOneOfCommitStreak).days + 1

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
    "12": "Weighed, and checked body composition.",
    "13": "Went through night routine."
}


def set_screen():
    global myScreen, td, topElements, events
    events = []
    topElements = [
        Button(root, command=partial(date_change, False), text="<--"),
        Label(root, text=""),
        Button(root, command=partial(date_change, True), text="-->"),
        Label(root, text="Intro"),
        Entry(root),
        Label(root, text="Goal"),
        Entry(root),
        Label(root, text="Conclusion"),
        Entry(root),
        Label(root, text="Change Event Total"),
        Button(root, command=add_activity, text="+"),
        Button(root, command=sub_activity, text="-")
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
    event_col = (len(events)//80)*2
    myGrid = [
        topElements[0].grid(row=0, column=0+event_col),
        topElements[1].grid(row=0, column=1+event_col),
        topElements[2].grid(row=0, column=2+event_col),
        topElements[3].grid(row=0, column=3+event_col),
        topElements[4].grid(row=0, column=4+event_col),
        topElements[5].grid(row=0, column=5+event_col),
        topElements[6].grid(row=0, column=6+event_col),
        topElements[7].grid(row=0, column=7+event_col),
        topElements[8].grid(row=0, column=8+event_col),
        topElements[9].grid(row=0, column=9+event_col),
        topElements[10].grid(row=0, column=10+event_col),
        topElements[11].grid(row=0, column=11+event_col)
    ]


def add_activity():
    if len(events) < 160:
        event_col = len(events) // 80
        events.append(Entry(root))
        events[-1].grid(row=int((((len(events) - 1) / 2) + 1)-40*event_col), column=0+event_col*2)
        events.append(Entry(root))
        events[-1].grid(row=int((((len(events) - 2) / 2) + 1)-40*event_col), column=1+event_col*2)
        if len(events) == 80:
            set_grid()


def sub_activity():
    if len(events) > 0:
        for i in range(2):
            events[-1].destroy()
            events.pop(-1)


root.title("Daily Log Tool")
set_screen()

root.mainloop()
