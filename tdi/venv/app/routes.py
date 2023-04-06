from flask import render_template, flash, redirect, request, session
from app import app, db
from app.forms import LogInForm, RegistrationForm, UserDetailsForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
#from werkzeug.urls import url_parse

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    
    form=LogInForm()

    if request.form.get('login_action') == 'Register Here':
               return redirect('/register')
    
    if form.validate_on_submit():
        user = User.query.filter_by(ashoka_email=form.login_mail.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        
        login_user(user, remember=form.remember_me.data)
        return redirect('/home')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/home')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(ashoka_email=form.login_mail.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/user_details')
    return render_template('registration.html', title='Register', form=form)

@app.route('/user_details', methods=['GET', 'POST'])
def user_details():
     form=UserDetailsForm()
     if form.validate_on_submit():
          current_user.name=form.name.data
          db.session.commit()
          flash('Please Login to Continue')
          return redirect('/login')
     elif request.method=='GET':
          form.name.data=current_user.name
     return render_template('user_details.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
        if request.method == 'POST':
            if request.form.get('home_action') == 'Meal Booking':
               return redirect('/mealbooking')
            if request.form.get('home_action') == 'Housekeeping':
               return redirect('/housekeeping')
            if request.form.get('home_action') == 'Maintenance Requests':
               return('Welcome to Maintenance Requests Page')
            if request.form.get('home_action') == 'Manage Requests':
               return('Welcome to Manage Requests Page')       
        elif request.method == 'GET':
            return render_template('home.html', title='Home')
        
@app.route('/mealbooking', methods=['GET', 'POST'])
@login_required      
def mealbooking():
        if request.method == 'POST':
            if request.form.get('meal_action') == 'Book':
               return redirect('/mealbooking_success')
            elif request.form.get('meal_action') == 'Cancel':
                return redirect('/home')
        elif request.method == 'GET':
            return render_template('mealbooking.html')
        
@app.route('/mealbooking_success', methods=['GET', 'POST'])
@login_required  
def mealbooking_success():
        if request.method == 'POST':
            if request.form.get('meal_success_action') == 'Book More':
               return redirect('/mealbooking')
            elif request.form.get('meal_success_action') == 'Home':
                return redirect('/home')
        elif request.method == 'GET':
            return render_template('mealbooking_success.html')        
     
@app.route('/housekeeping', methods=['GET', 'POST'])
@login_required
def housekeeping():
         if request.method == 'POST':
            if request.form.get('housekeeping_action') == 'Submit':
               return redirect('/housekeeping_success')
            elif request.form.get('housekeeping_action') == 'Cancel':
                return redirect('/home')
         elif request.method == 'GET':
            return render_template('housekeeping.html')
         
@app.route('/housekeeping_success', methods=['GET', 'POST'])
@login_required
def housekeeping_success():
        if request.method == 'POST':
            if request.form.get('housekeeping_success_action') == 'Home':
                return redirect('/home')
        elif request.method == 'GET':
            return render_template('housekeeping_success.html')       
