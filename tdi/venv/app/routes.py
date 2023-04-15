from flask import render_template, flash, redirect, request, session
from app import app, db
from app.forms import LogInForm, RegistrationForm, UserDetailsForm, MealForm, EditProfileForm
from app.models import User, Housekeeping, Maintenance, Requests
from flask_login import current_user, login_user, logout_user, login_required
from datetime import date, datetime
from werkzeug.urls import url_parse

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    form=LogInForm()
    if request.form.get('login_action') == 'Register Here':
               return redirect('/register')
    
    if form.validate_on_submit():
        user = User.query.filter_by(ashoka_id=form.ashoka_id.data).first()
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
        user = User(ashoka_id=form.ashoka_id.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Please Login to Continue')
        return redirect('/login')
    return render_template('registration.html', title='Register', form=form)


@app.route('/user_details', methods=['GET', 'POST'])
def user_details():
     #if request.method == 'POST':
     #    floor=request.form.get('floor')
     form=UserDetailsForm()
     if form.validate_on_submit():
          current_user.name=form.name.data
          current_user.ashoka_email=form.ashoka_email.data
          current_user.flat=str(form.flat.data) + " " + str(request.form.get('floor'))
          current_user.room=form.room.data
          db.session.commit()
          return redirect('/login')
     elif request.method=='GET':
          return render_template('user_details.html', title='Register', form=form)
     
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.flat[-2:] == 'GF':
         floor='Ground Floor'
         short_floor='GF'
    elif current_user.flat[-2:] == 'FF':
         floor='First Floor'
         short_floor='FF'
    elif current_user.flat[-2:] == 'SF':
         floor='Second Floor'
         short_floor='SF'
    elif current_user.flat[-2:] == 'TF':
         floor='Third Floor'
         short_floor='TF'
    elif current_user.flat[-6:] == 'Duplex':
         floor='Duplex' 
         short_floor=floor                  

    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.room = form.room.data
        current_user.ashoka_id = form.ashoka_id.data
        current_user.ashoka_email=form.ashoka_email.data
        #if request.form.get('floor') != 'same':      
        current_user.flat=str(form.flat.data) + " " + str(request.form.get('floor'))
        db.session.commit()
        flash('Your profile has been updated')
        return redirect('/edit_profile')
    
    #elif request.method=='GET':
    else:
        form.name.data = current_user.name
        form.flat.data = current_user.flat[:3] #Good Practice?
        form.ashoka_id.data = current_user.ashoka_id
        form.room.data = current_user.room
        form.ashoka_email.data = current_user.ashoka_email
        return render_template('edit_profile.html', title='Edit Profile', form=form, floor=floor, short_floor=short_floor)
######## Everything works but check html for red brackets #######


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
        if current_user.name == None:
             return redirect('/user_details')
        elif request.method == 'POST':
            if request.form.get('home_action') == 'Meal Booking':
               return redirect('/mealbooking')
            if request.form.get('home_action') == 'Housekeeping':
               return redirect('/housekeeping')
            if request.form.get('home_action') == 'Maintenance Requests':
               return redirect('/maintenance_request')
            if request.form.get('home_action') == 'Manage Requests':
               return redirect('/manage_requests')      
        elif request.method == 'GET':
            return render_template('home.html', title='Home')        
        
@app.route('/mealbooking', methods=['GET', 'POST'])
@login_required      
def mealbooking():
        form=MealForm()
        if form.validate_on_submit():
            return redirect('/mealbooking_success')
        return render_template('mealbooking.html', title='Meal Booking', form=form)
      
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
                db.session.add(Housekeeping(name=current_user.name, ashoka_id=current_user.ashoka_id, flat=current_user.flat, room=current_user.room, time_slot=request.form.get('time_slot'), body=request.form.get('remarks')))
                db.session.add(Requests(name=current_user.name, ashoka_id=current_user.ashoka_id, flat=current_user.flat, room=current_user.room, time_slot=request.form.get('time_slot'), body=request.form.get('remarks'), type='Housekeeping'))
                db.session.commit()
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

@app.route('/maintenance_request', methods=['GET', 'POST'])
@login_required
def maintenance_request():
         if request.method == 'POST':
            if request.form.get('maintenance_action') == 'Submit':
                db.session.add(Maintenance(name=current_user.name, ashoka_id=current_user.ashoka_id, flat=current_user.flat, room=current_user.room, body=request.form.get('request')))
                db.session.add(Requests(name=current_user.name, ashoka_id=current_user.ashoka_id, flat=current_user.flat, room=current_user.room, body=request.form.get('request'), type='Maintenance'))
                db.session.commit()
                return redirect('/maintenance_request_success')
            elif request.form.get('maintenance_action') == 'Cancel':
                return redirect('/home')
         elif request.method == 'GET':
            return render_template('maintenance_request.html')
               
@app.route('/maintenance_request_success', methods=['GET', 'POST'])
@login_required
def maintenance_success():
        if request.method == 'POST':
            if request.form.get('maintenance_success_action') == 'Home':
                return redirect('/home')
        elif request.method == 'GET':
            return render_template('maintenance_request_success.html') 
        
@app.route('/manage_requests', methods=['GET', 'POST'])
@login_required      
def manage_requests():
         print(Requests.query.filter_by(ashoka_id=current_user.ashoka_id).all())
         return

@app.route('/goodboii')
def goodboii():
    return render_template('TDILogin.html')

@app.route('/page0')
def page0():
    return render_template('page0.html')

@app.route('/page01', methods=['GET', 'POST'])
def page01():
  
    form=LogInForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(ashoka_email=form.login_mail.data).first()
        if user is None:
            flash('Invalid username')
            return redirect('/page01')
        
        login_user(user, remember=form.remember_me.data)
        return redirect('/home')
    return render_template('page01.html', title='Sign In', form=form)

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    return render_template('page3.html')