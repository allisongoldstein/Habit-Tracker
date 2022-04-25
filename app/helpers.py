from datetime import date
import calendar

def getMonthCalendar():
    today = date.today()
    print(today)
    print('this', today.month)
    cal = calendar.month(today.year, today.month)
    monthCal = calendar.HTMLCalendar(firstweekday=0)
    month, year = today.month, today.year
    printMonth = monthCal.formatmonth(year, month)
    return printMonth
