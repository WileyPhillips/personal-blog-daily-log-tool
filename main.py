from functools import partial
from tkinter import *
from datetime import date, timedelta, datetime
from tkinter.scrolledtext import ScrolledText


# TODO blank label
# TODO look into adding a new window
# TODO make it so clear log doesn't reset the date

bgColor = "#93C7D3"

root = Tk()
root.geometry("1920x1080")
root.configure(bg=bgColor)

# streak is shown in the output, but not in the GUI
dayOneOfDailyLogStreak = datetime(2021, 9, 26)
dayOneOfCommitStreak = datetime(2021, 11, 5)
streaks = [dayOneOfDailyLogStreak, dayOneOfCommitStreak]

resultOutput = ""
blankEndTime = False
currentLog = []
lastEventIndex = 0
firstTime = True
numEvents = 17
strNum = ["1", "2", "3", "4", "5", "6", "7", "8", "9", ]


def date_change(up):
    global td, yesterday, firstSlash, secondSlash, today, dailyLogStreak, commitStreak
    if up:
        # arrow to the right of date label was hit, and will lead to the date becoming one day later
        td = td + timedelta(days=1)
    else:
        # arrow to the left of date label was hit, and will lead to the date becoming one day earlier
        td = td - timedelta(days=1)
    yd = td - timedelta(days=1)
    today = td.strftime("%m/%d/%Y")
    yesterday = yd.strftime("%m/%d/%Y")

    firstSlash = yesterday.find("/")
    secondSlash = yesterday[firstSlash + 1:].find("/") + firstSlash
    first_slash_today = today.find("/")
    second_slash_today = today[firstSlash + 1:].find("/") + first_slash_today

    """ 
    For GUI and output formatting as the 9th for example won't display "09" in the link or label but will prior
    to the if statements underneath
    """
    if today[first_slash_today + 1] == "0":
        today = today[:first_slash_today+1] + today[first_slash_today+2:]
        second_slash_today = today[firstSlash + 1:].find("/") + first_slash_today
    if yesterday[firstSlash + 1] == "0":
        yesterday = yesterday[:firstSlash + 1] + yesterday[firstSlash + 2:]
        secondSlash = yesterday[firstSlash + 1:].find("/") + firstSlash

    td_as_date_time = datetime(int(today[-4:]), int(today[:first_slash_today]),
                               int(today[first_slash_today + 1:second_slash_today + 1]))
    dailyLogStreak = (td_as_date_time - dayOneOfDailyLogStreak).days + 1
    commitStreak = (td_as_date_time - dayOneOfCommitStreak).days + 1
    # the date shown in the top left
    topElements[1].config(text=today, bg=bgColor)


# to save time on activities that are expected to occur often
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


# prints dictionary into GUI, so shorthand doesn't need to be memorized
def set_shorthand():
    for i in range(len(shortHandDict)):
        short_hand_text = str(i+1) + " - " + shortHandDict.get(str(i+1))
        short_hand_label = Label(root, text=short_hand_text)
        short_hand_label.grid(row=2+i, column=7)
        short_hand_label.configure(bg=bgColor)


def set_screen():
    global td, topElements, events, numEntry
    # variable, and controlled via event add/subtract buttons
    text_entry = StringVar()
    text_entry.set("Woke up.")
    events = [
        Entry(root),
        Entry(root, textvariable=text_entry)
    ]
    # the same each time
    numEntry = StringVar()
    numEntry.set("1")
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
        Entry(root, width=4, textvariable=numEntry),
        Button(root, command=sub_activity, text="-"),
        Button(root, command=copy_log, text="copy"),
        Button(root, command=clear_log, text="clear"),
        ScrolledText(root, wrap=None, width=20),
        Button(root, command=format_phone_log, text="populate")
    ]
    set_grid()
    configure_labels()
    set_shorthand()
    td = date.today()
    td = td - timedelta(days=1)
    date_change(True)


# makes all labels within topElements the background color, so that there isn't a white box surrounding them
def configure_labels():
    global topElements
    for i in range(len(topElements)):
        if type(topElements[i]) == Label:
            topElements[i].configure(bg=bgColor)


def set_grid():
    global myGrid, topElements
    # will be used in conjunction with a label of spaces so the add activity button doesn't move at a threshold
    event_col = len(events) > (numEvents*2)
    for i in range(13):
        topElements[i].grid(row=0, column=i)
    topElements[13].grid(row=1, column=7)
    topElements[14].grid(row=3+len(shortHandDict), column=7)
    topElements[15].grid(row=1, column=13)
    topElements[16].grid(row=2, column=13)
    events[0].grid(row=1, column=0)
    events[1].grid(row=1, column=1)


def clear_log():
    # deletes all added activities
    for i in range(len(events)-2):
        sub_activity()
    # clears entries and gets everything back to the starting point
    set_screen()


def add_activity():
    iterations = activity_iterations()
    for i in range(iterations):
        if len(events) < numEvents * 4:
            event_col = len(events) // (numEvents * 2)
            events.append(Entry(root))
            events[-1].grid(row=int((((len(events) - 1) / 2) + 1)-numEvents*event_col), column=0+event_col*2)
            events.append(Entry(root))
            events[-1].grid(row=int((((len(events) - 2) / 2) + 1)-numEvents*event_col), column=1+event_col*2)
            # in order to move elements over at event thresholds
            if len(events) == numEvents * 2:
                set_grid()
        else:
            break


def sub_activity():
    iterations = activity_iterations()
    for i in range(iterations):
        if len(events) > 2:
            for j in range(2):
                events[-1].destroy()
                events.pop(-1)
        else:
            print("yes")
            break


def activity_iterations():
    try:
        return int(topElements[11].get())
    except:
        numEntry.set("1")
        return 1


def format_phone_log():
    log = topElements[15].get("1.0", "end-1c")
    log = log.split("\n")
    if log[1] == "":
        log.pop(1)
    log_placeholder = []
    if "" in log:
        for i in range(len(log)):
            if log[i] != "":
                log_placeholder.append(log[i])
    log = log_placeholder
    print(log)


def copy_log():
    result_output = "Daily Log - " + today + "\n"
    result_output += "Access Daily Log - {} http://wileyphillips.com/daily-log-{}".format(yesterday, yesterday[:2])
    result_output += "-{}-{}/\n\n".format(yesterday[firstSlash + 1: secondSlash+1], yesterday[-4:])
    result_output += "Current Streak: Daily Log - {}, Commit - {}\n\n".format(str(dailyLogStreak), str(commitStreak))
    result_output += "{}\nToday's Goal: {}\n\n".format(topElements[4].get(), topElements[6].get())
    last_time = events[0].get()
    # entry starts as "Woke up.", if changed the time format will be that of me being awake at midnight
    if events[1].get() == "Woke up.":
        result_output += last_time + ": " + "Woke up.\n"
    else:
        # if first activity isn't waking up this checks if it is a activity with a shorthand
        activity = events[1].get()
        if activity in shortHandDict:
            activity = shortHandDict.get(activity)
        result_output += "12:00am - {}: {}\n".format(last_time, activity)
    for i in range(int(len(events[2:]) / 2)):
        new_time = events[i * 2 + 2].get()
        activity = events[i * 2 + 3].get()
        if activity in shortHandDict:
            activity = shortHandDict.get(activity)
        result_output += "{} - {}: {}\n".format(last_time, str(new_time), str(activity))
        last_time = new_time
    result_output += last_time + ": Went to sleep.\n\n"
    result_output += "In Closing: " + topElements[8].get()

    # replaces whatever is currently copied to clipboard with the new daily log.
    root.clipboard_clear()
    root.clipboard_append(result_output)


root.title("Daily Log Tool")
set_screen()

root.mainloop()
