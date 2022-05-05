import calendar
from calendar import HTMLCalendar, firstweekday

class CustomCal(HTMLCalendar):
    def __init__(self, month, year):
        super(HTMLCalendar).__init__()
        self.firstweekday = 6
        self.month = month
        self.year = year


    def formatday(self, day, weekday):
        day2 = str(day)
        month = str(self.month)
        year = str(self.year)
        if len(day2) == 1:
            day2 = '0' + day2
        if len(month) == 1:
            month = '0' + month
        date = year + '-' + month + '-' + day2 
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        else:
            return '<td class="%s" id="calDate"><a class="calDate" href="javascript:f();" name="%s">%d</a></td>' % (self.cssclasses[weekday], date, day)


def getMonthCalendar(date):
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

    print(editedCal)

    return editedCal
