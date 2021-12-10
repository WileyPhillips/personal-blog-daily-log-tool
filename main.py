import datetime
from functools import partial
from tkinter import *
# from tkinter.ttk import *
from datetime import date, timedelta, datetime



# TODO look into adding a new window

bgColor = "#93C7D3"

root = Tk()
root.geometry("1920x1080")
root.configure(bg=bgColor)

# Streak is shown in the output, but not in the GUI
dayOneOfDailyLogStreak = datetime(2021, 9, 26)
dayOneOfCommitStreak = datetime(2021, 11, 5)
streaks = [dayOneOfDailyLogStreak, dayOneOfCommitStreak]

resultOutput = ""
blankEndTime = False
currentLog = []
lastEventIndex = 0
firstTime = True
numEvents = 38



def date_change(up):
    global td, yesterday, firstSlash, secondSlash, today, dailyLogStreak, commitStreak
    if up:
        td = td + timedelta(days=1)
    else:
        td = td - timedelta(days=1)
    yd = td - timedelta(days=1)
    today = td.strftime("%m/%d/%Y")
    yesterday = yd.strftime("%m/%d/%Y")

    firstSlash = yesterday.find("/")
    secondSlash = yesterday[firstSlash + 1:].find("/") + firstSlash
    first_slash_today = today.find("/")
    second_slash_today = today[firstSlash + 1:].find("/") + first_slash_today

    # For GUI and output formatting
    if today[first_slash_today + 1] == "0":
        today = today[:first_slash_today+1] + today[first_slash_today+2:]
        second_slash_today = today[firstSlash + 1:].find("/") + first_slash_today
    # For output formatting
    if yesterday[firstSlash + 1] == "0":
        yesterday = yesterday[:firstSlash + 1] + yesterday[firstSlash + 2:]
        secondSlash = yesterday[firstSlash + 1:].find("/") + firstSlash

    td_as_date_time = datetime(int(today[-4:]), int(today[:first_slash_today]),
                               int(today[first_slash_today + 1:second_slash_today + 1]))
    dailyLogStreak = (td_as_date_time - dayOneOfDailyLogStreak).days + 1
    commitStreak = (td_as_date_time - dayOneOfCommitStreak).days + 1
    # The date shown in the top left
    topElements[1].config(text=today, bg=bgColor)


# To save time on activities that are expected to occur often
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
    "10": "Ate dinner.",
    "11": "Had a snack.",
    "12": "Weighed, and checked body composition.",
    "13": "Did some cleaning.",
    "14": "Went through night routine."
}


# Prints dictionary into GUI, so shorthand doesn't need to be memorized.
def set_shorthand():
    for i in range(len(shortHandDict)):
        short_hand_text = str(i+1) + " - " + shortHandDict.get(str(i+1))
        short_hand_label = Label(root, text=short_hand_text)
        short_hand_label.grid(row=2+i, column=7)
        short_hand_label.configure(bg=bgColor)


def set_screen():
    global td, topElements, events
    # Variable, and controlled via event add/subtract buttons
    textEntry = StringVar()
    textEntry.set("Woke up.")
    events = [
        Entry(root),
        Entry(root, textvariable=textEntry)
    ]
    # The same each time
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
        Button(root, command=sub_activity, text="-"),
        Button(root, command=copy_log, text="copy")
    ]
    set_grid()
    configure_labels()
    set_shorthand()
    td = date.today()
    td = td - timedelta(days=1)
    date_change(True)


def configure_labels():
    global topElements
    for i in range(len(topElements)):
        if type(topElements[i]) == Label:
            topElements[i].configure(bg=bgColor)


def set_grid():
    global myGrid, topElements
    event_col = (len(events)//(numEvents*2))*2
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
        topElements[11].grid(row=0, column=11+event_col),
        topElements[12].grid(row=1, column=7),
        events[0].grid(row=1, column=0),
        events[1].grid(row=1, column=1)
    ]


def add_activity():
    if len(events) < numEvents * 4:
        event_col = len(events) // (numEvents * 2)
        events.append(Entry(root))
        events[-1].grid(row=int((((len(events) - 1) / 2) + 1)-numEvents*event_col), column=0+event_col*2)
        events.append(Entry(root))
        events[-1].grid(row=int((((len(events) - 2) / 2) + 1)-numEvents*event_col), column=1+event_col*2)
        # In order to move elements over at event thresholds
        if len(events) == numEvents * 2:
            set_grid()


def sub_activity():
    if len(events) > 2:
        for i in range(2):
            events[-1].destroy()
            events.pop(-1)


def copy_log():
    # Time that they woke
    result_output = "Daily Log - " + today + "\n"
    result_output += "Access Daily Log - " + yesterday + " http://wileyphillips.com/daily-log-" + yesterday[:2]
    result_output += "-" + yesterday[firstSlash + 1:secondSlash + 1] + "-" + yesterday[-4:] + "/\n\n"
    result_output += "Current Streak: Daily Log - " + str(dailyLogStreak) + ", Commit - " + str(commitStreak) + "\n\n"
    result_output += topElements[4].get() + "\nToday's Goal: " + topElements[6].get() + "\n\n"
    last_time = events[0].get()
    if events[1].get() == "Woke up.":
        result_output += last_time + ": " + "Woke up.\n"
    else:
        result_output += "12:00am - " + last_time + ": " + events[1].get() + "\n"
    for i in range(int(len(events[2:]) / 2)):
        new_time = events[i * 2 + 2].get()
        activity = events[i * 2 + 3].get()
        if activity in shortHandDict:
            activity = shortHandDict.get(activity)
        result_output += last_time + " - " + str(new_time) + ": " + str(activity) + "\n"
        last_time = new_time
    result_output += last_time + ": Went to sleep.\n\n"
    result_output += "In Closing: " + topElements[8].get()

    root.clipboard_clear()
    root.clipboard_append(result_output)


root.title("Daily Log Tool")
set_screen()

root.mainloop()
