from app import app, db
from flask import jsonify, render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, AddTaskForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Task
from datetime import date



@app.route('/')
@app.route('/index')
def index():
    today = date.today()
    strdate = today.strftime('%B %d, %Y')
    tasks = Task.query.all()
    checkedTasks = Task.query.filter_by(completed=True, date=today).all()
    uncheckedTasks = []
    for task in tasks:
        if task not in checkedTasks:
            uncheckedTasks.append(task)
    print(uncheckedTasks)
    print(checkedTasks)
    return render_template('index.html', title='Habit Tracker', date=strdate, tasks=uncheckedTasks, completedTasks=checkedTasks)

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

@app.route('/viewTasks')
def viewTasks():
    tasks = Task.query.all()
    checkedTasks = Task.query.filter_by(completed=True).all()
    uncheckedTasks = []
    for task in tasks:
        if task not in checkedTasks:
            uncheckedTasks.append(task)
    print(uncheckedTasks)
    print(checkedTasks)
    showDelete = False
    return render_template('viewTasks.html', title='View Tasks', tasks=uncheckedTasks, completedTasks=checkedTasks, showDelete=showDelete)

@app.route('/addTask', methods=['GET', 'POST'])
def addTask():
    form = AddTaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data)
        db.session.add(task)
        db.session.commit()
        flash('Task added.')
        return redirect(url_for('index'))
    return render_template('addTask.html', title='Add Task', form=form)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        task = Task(name=name, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
    return 'success'

@app.route('/check', methods=['GET', 'POST'])
def check():
    print('testerrrrrrrrrrrrrrrrr')
    if request.method == 'POST':
        id = request.form['id']
        checked = request.form['checked']
        today = date.today()
        task = Task.query.filter_by(id=id).first()
        if checked == 'checked':
            task.completed = True
            task.date = today
        else:
            task.completed = False
        db.session.commit()

    return 'success'

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    print('test')
    if request.method == 'POST':
        print(request.method)
        print(request.form)
        id = request.form['id']
        print(id)
        task = Task.query.filter_by(id=id).first()
        db.session.delete(task)
        db.session.commit()
        return 'success'
