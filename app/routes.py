from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, Habit, Check
from datetime import date, datetime, timedelta
from app.helpers import *


@app.route('/')
@app.route('/index')
def index():
    """
    Redirects to viewDate (today),
    redirects to login if not logged in
    """
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    return redirect(url_for('viewDate'))

@login_required
@app.route('/viewDate/<viewDate>')
@app.route('/viewDate/')
def viewDate(viewDate=None):
    """Displays viewDate data, defaults to today"""
    if viewDate is None:
        viewDate = date.today()
    else:
        viewDate = datetime.strptime(viewDate, '%Y-%m-%d').date()
    prevDate, nextDate = viewDate - timedelta(1), viewDate + timedelta(1)     # for prev/next day links
    strDate = viewDate.strftime('%B %d, %Y')
    habits = Habit.query.filter_by(user_id=current_user.id)
    checks = Check.query.filter_by(user_id=current_user.id, date=viewDate).all()
    checkedHabits = []
    uncheckedHabits = []
    for check in checks:
        habit = Habit.query.filter_by(id=check.habit_id).first()
        checkedHabits.append(habit)
    for habit in habits:
        if habit not in checkedHabits:
            uncheckedHabits.append(habit)
    month = getMonthCalendar(viewDate)

    return render_template('index.html', title='Habit Tracker',
    date=viewDate, prevDate=prevDate, nextDate=nextDate, strDate=strDate, month=month,
    habits=uncheckedHabits, completedHabits=checkedHabits)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@login_required
@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add new habit"""
    if request.method == 'POST':
        name = request.form['name']
        habit = Habit(name=name, user_id=current_user.id)
        db.session.add(habit)
        db.session.commit()
    return 'success'

@login_required
@app.route('/check', methods=['GET', 'POST'])
def check():
    """Check or uncheck habits based on current status for selected date"""
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%B %d, %Y').date()
        if date > date.today():
            return redirect(url_for('viewDate', viewDate=date))     # future date redirects to today
        id = request.form['id']
        checked = request.form['checked']
        if checked == 'checked':
            check = Check(habit_id=id, user_id=current_user.id, date=date)
            db.session.add(check)
        else:                                                       # uncheck
            check = Check.query.filter_by(habit_id=id, user_id=current_user.id).first()
            db.session.delete(check)
        db.session.commit()

    return 'success'

@login_required
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    """Delete habit"""
    if request.method == 'POST':
        id = request.form['id']
        habit = Habit.query.filter_by(id=id).first()
        db.session.delete(habit)
        db.session.commit()
        return 'success'

@login_required
@app.route('/viewStats/')
@app.route('/viewStats/<range>')
def viewStats(range=30):
    """Generate stats for given range"""
    try:
        numRange = int(range)
        type = 'range'
    except:
        type = 'month'
        month = range.rstrip('1234567890')
        year = range[len(month):]
        print('range =', month, year)

    month = getMonthCalendar(datetime.today())
    statsList = getStats(30)
    for stat in statsList:          # append completion % to habit stats list
        stat.append(round(stat[2]/range * 100))

    return render_template('viewStats.html', title='View Stats',
    stats=statsList, type=type, days=range, month=month)

@login_required
@app.route('/habitStats/<habit_id>')
def habitStats(habit_id):
    month = getMonthCalendar(datetime.today())
    habit = Habit.query.filter_by(id=habit_id).first()
    name = habit.name

    title = 'Stats for {}'.format(name)
    months, days, stats = getHabitStats(habit_id, 4)
    imgurls = getImage(name)
    imgurls = imgurls.splitlines()

    return render_template('habitStats.html', title=title, name=name,
    stats=stats, days=days, months=months, month=month,
    imgurls=imgurls)
