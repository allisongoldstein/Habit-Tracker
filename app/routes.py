from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Habit, Check
from datetime import date, datetime
from app.helpers import *


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    viewDate = date.today()
    strdate = viewDate.strftime('%B %d, %Y')
    habits = Habit.query.filter_by(user_id=current_user.id)
    checks = Check.query.filter_by(user_id=current_user.id, date=viewDate).all()
    checkedHabits = []
    uncheckedHabits = []
    for check in checks:
        habit = Habit.query.filter_by(id=check.habit_id).first()
        print(habit)
        checkedHabits.append(habit)
    for habit in habits:
        if habit not in checkedHabits:
            uncheckedHabits.append(habit)
    print('checks: ', checkedHabits)
    print('uc: ', uncheckedHabits)
    month = getMonthCalendar()
    return render_template('index.html', title='Habit Tracker',
    date=strdate, month=month,
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

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        habit = Habit(name=name, user_id=current_user.id)
        db.session.add(habit)
        db.session.commit()
    return 'success'

@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        id = request.form['id']
        checked = request.form['checked']
        date = datetime.strptime(request.form['date'], '%B %d, %Y').date()
        if checked == 'checked':
            check = Check(habit_id=id, user_id=current_user.id, date=date)
            db.session.add(check)
        else:
            check = Check.query.filter_by(habit_id=id, user_id=current_user.id).first()
            db.session.delete(check)
        db.session.commit()

    return 'success'

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        id = request.form['id']
        habit = Habit.query.filter_by(id=id).first()
        db.session.delete(habit)
        db.session.commit()
        return 'success'

@app.route('/viewDate/<viewDate>')
@app.route('/viewDate/')
def viewDate(viewDate=None):
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    if viewDate is None:
        return redirect(url_for('index'))
    else:
        viewDate = datetime.strptime(viewDate, '%Y-%m-%d').date()  
    strdate = viewDate.strftime('%B %d, %Y')
    habits = Habit.query.filter_by(user_id=current_user.id)
    checks = Check.query.filter_by(user_id=current_user.id, date=viewDate).all()
    checkedHabits = []
    uncheckedHabits = []
    for check in checks:
        habit = Habit.query.filter_by(id=check.habit_id).first()
        print(habit)
        checkedHabits.append(habit)
    for habit in habits:
        if habit not in checkedHabits:
            uncheckedHabits.append(habit)
    print('checks: ', checkedHabits)
    print('uc: ', uncheckedHabits)
    month = getMonthCalendar()
    return render_template('index.html', title='Habit Tracker',
    date=strdate, month=month,
    habits=uncheckedHabits, completedHabits=checkedHabits)
