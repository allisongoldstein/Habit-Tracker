from datetime import date
import calendar

def getMonthCalendar():
    today = date.today()
    month, year = today.month, today.year

    cal = calendar.month(today.year, today.month)
    monthCal = calendar.HTMLCalendar(firstweekday=0)
    calHTML = monthCal.formatmonth(year, month)

    display = '<b><span class="today">' + str(today.day) + '</span></b>'
    editedCal = calHTML.replace(str(today.day), display)
    
    return editedCal
