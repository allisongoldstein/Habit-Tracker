from calendar import HTMLCalendar
from random import getstate
from flask_login import current_user
from app.models import Habit, Check
from datetime import date
from time import strptime
import time
import calendar
import matplotlib.pyplot as plt

class CustomCal(HTMLCalendar):
    def __init__(self, month, year):
        super(HTMLCalendar).__init__()
        self.firstweekday = 6
        self.month = month
        self.year = year

    def formatday(self, day, weekday):
        """Add links to calendar display"""
        strDay = str(day)
        month = str(self.month)
        year = str(self.year)
        if len(strDay) == 1:
            strDay = '0' + strDay
        if len(month) == 1:
            month = '0' + month
        date = year + '-' + month + '-' + strDay
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        else:
            return '<td class="%s" id="calDate"><a class="calDate" href="javascript:f();" name="%s">%d</a></td>' % (self.cssclasses[weekday], date, day)


def getMonthCalendar(date):
    """
    Returns HTML calendar
    Highlights today and/or current day
    """
    month, year = date.month, date.year
    today = date.today()

    calHTML = CustomCal(month, year).formatmonth(year, month)
    editedCal = calHTML

    if month == today.month and year == today.year:
        editDate = '>' + str(today.day) + '<'
        display = '><b><span class="today">  ' + str(today.day) + '  </span></b><'
        editedCal = calHTML.replace(str(editDate), display)
    editDate = '>' + str(date.day) + '<'
    display = '><span id="onDate">  ' + str(date.day) + '  </span><'
    editedCal = editedCal.replace(str(editDate), display)

    return editedCal

def getStats(range=0, statHabit=None):
    """
    Returns stats: list of habit stats for given date range
    For each habit append [id, name, count]
    """
    today = date.today()
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    statsList = []
    try:
        int(range)
        for habit in habits:
            habitStats = [habit.id, habit.name, 0]
            checks = Check.query.filter_by(user_id=current_user.id, habit_id=habit.id).all()
            for check in checks:
                if (today - check.date).days <= range:
                    habitStats[2] += 1
            statsList.append(habitStats)
    except:
        range = range.split(' ')
        month, year = range[0], range[1]
        intMonth, intYear = strptime(month, '%B').tm_mon, int(year)
        displayMonth = month + ' ' + year
        if statHabit:
            checks = Check.query.filter_by(user_id=current_user.id, habit_id=statHabit.id).all()
        else:
            checks = Check.query.filter_by(user_id=current_user.id, habit_id=habit.id).all()
        count, total = 0, calendar.monthrange(intYear, intMonth)[1]
        if intMonth == today.month and intYear == today.year:           # percent up to today for current month
            total = today.day  
        
        for check in checks:
            if check.date.month == intMonth and check.date.year == intYear:
                count += 1
        statsList = [displayMonth, [count, total]]

    return statsList

def getHabitStats(id=1, numMonths=4):
    """
    Returns list of month names for previous numMonths and list of habitPercentages of completion
    """
    habit = Habit.query.filter_by(id=id).first()
    month, year = date.today().month, date.today().year
    monthList = [calendar.month_name[month] + ' ' + str(year)]
    for _ in range(1, numMonths):
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        monthList.insert(0, calendar.month_name[month] + ' ' + str(year))
    habitPercentages = []
    dayCount = []
    for month in monthList:
        stats = getStats(month, habit)
        days = stats[1]
        dayCount.append(days)
        habitPercentages.append(round(stats[1][0]/stats[1][1] * 100))
    monthList[-1] += '*'
    return monthList, dayCount, habitPercentages

def getImage(text):
    text += ' clip art'
    with open('../ms5/ms5.txt', 'w') as f:
        f.write('runTheFollowing1' + text)
    time.sleep(1)
    with open('../ms5/ms5.txt', 'r') as fr:
        imgs = fr.read()
        # print(imgs)

    return imgs
