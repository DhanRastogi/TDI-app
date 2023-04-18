from flask import render_template, flash, redirect, request, session, url_for
from app import app, db
from app.forms import LogInForm, RegistrationForm, UserDetailsForm, MealForm, EditProfileForm, HouseForm, MaintenanceForm, HouseEditForm
from app.models import User, Housekeeping, Maintenance, Requests
from flask_login import current_user, login_user, logout_user, login_required
from datetime import date, datetime
from werkzeug.urls import url_parse

########## Back Space problem ##########

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LogInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(ashoka_id=form.ashoka_id.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)

        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('home'))
        
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(ashoka_id=form.ashoka_id.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)


@app.route('/user_details', methods=['GET', 'POST'])
def user_details():
    if current_user.ashoka_id == 1000:
        return redirect(url_for('admin'))

    form=UserDetailsForm()
    if form.validate_on_submit():
          current_user.name=form.name.data
          current_user.ashoka_email=form.ashoka_email.data
          current_user.flat=str(form.flat.data) + " " + str(request.form.get('floor'))
          current_user.room=form.room.data
          db.session.commit()
          return redirect(url_for('login'))
    else:
          return render_template('user_details.html', title='Register', form=form)
     
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if current_user.ashoka_id != 1000:
        logout_user()
        return redirect(url_for('login'))
    

    if request.method == 'GET':
        hk_req=Housekeeping.query.all()
        hk_req.reverse()
        main_req=Maintenance.query.all()
        main_req.reverse()
        return render_template('admin_home.html', hk_requests=hk_req, main_requests=main_req)
         
########## ADMIN ERROR PAGE SHOWS PROFILE AND HOME IN THE NAVIGATION BAR ##########    
     
@app.route('/edit_profile/<id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    if current_user.ashoka_id == 1000:
        return redirect(url_for('admin'))
    
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
         short_floor='Duplex'               

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
        return redirect(url_for('edit_profile', id=current_user.ashoka_id))
    
    #elif request.method=='GET':
    else:
        form.name.data = current_user.name
        form.flat.data = current_user.flat[:3] #Good Practice?
        form.floor.data = short_floor
        form.ashoka_id.data = current_user.ashoka_id
        form.room.data = current_user.room
        form.ashoka_email.data = current_user.ashoka_email
        return render_template('edit_profile.html', title='Edit Profile', form=form, floor=floor, short_floor=short_floor)
######## Everything works but check html for red brackets #######


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))

        if current_user.name == None:
             return redirect(url_for('user_details'))
        elif request.method == 'POST':
            if request.form.get('home_action') == 'Meal Booking':
               return redirect(url_for('mealbooking'))
            if request.form.get('home_action') == 'Housekeeping':
               return redirect(url_for('housekeeping'))
            if request.form.get('home_action') == 'Maintenance Requests':
               return redirect(url_for('maintenance_request'))
            if request.form.get('home_action') == 'Manage Requests':
               return redirect(url_for('manage_requests'))
        elif request.method == 'GET':
            return render_template('home.html', title='Home')        
        
@app.route('/mealbooking', methods=['GET', 'POST'])
@login_required      
def mealbooking():
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))

        form=MealForm()
        if form.validate_on_submit():
            return redirect(url_for('mealbooking_success'))
        return render_template('mealbooking.html', title='Meal Booking', form=form)
      
@app.route('/mealbooking_success', methods=['GET', 'POST'])
@login_required  
def mealbooking_success():
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))

        if request.method == 'POST':
            if request.form.get('meal_success_action') == 'Book More':
               return redirect(url_for('mealbooking'))
            elif request.form.get('meal_success_action') == 'Home':
                return redirect(url_for('home'))
        elif request.method == 'GET':
            return render_template('mealbooking_success.html')        
     
@app.route('/housekeeping', methods=['GET', 'POST'])
@login_required
def housekeeping():
         form=HouseForm()
         if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
         
         if form.validate_on_submit():
                db.session.add(Housekeeping(name=current_user.name, ashoka_id=current_user.ashoka_id, flat=current_user.flat, room=current_user.room, date=datetime.now().strftime('%d-%m-%Y'), time=datetime.now().strftime('%H:%M'), time_slot=form.time_slot.data, body=form.remarks.data))
                db.session.add(Requests(name=current_user.name, ashoka_id=current_user.ashoka_id, flat=current_user.flat, room=current_user.room, date=datetime.now().strftime('%d-%m-%Y'), time=datetime.now().strftime('%H:%M'), time_slot=form.time_slot.data, body=form.remarks.data, type='Housekeeping'))
                db.session.commit()
                return redirect(url_for('housekeeping_success'))
         else:
            return render_template('housekeeping.html', form=form)
         
@app.route('/housekeeping_success', methods=['GET', 'POST'])
@login_required
def housekeeping_success():
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
        
        if request.method == 'POST':
            if request.form.get('housekeeping_success_action') == 'Home':
                return redirect(url_for('home'))
        elif request.method == 'GET':
            return render_template('housekeeping_success.html')       

@app.route('/maintenance_request', methods=['GET', 'POST'])
@login_required
def maintenance_request():
         if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
         
         form=MaintenanceForm()
         if form.validate_on_submit():
                db.session.add(Maintenance(name=current_user.name, ashoka_id=current_user.ashoka_id, flat=current_user.flat, room=current_user.room, date=datetime.now().strftime('%d-%m-%Y'), time=datetime.now().strftime('%H:%M'), body=form.remarks.data))
                db.session.add(Requests(name=current_user.name, ashoka_id=current_user.ashoka_id, flat=current_user.flat, room=current_user.room, date=datetime.now().strftime('%d-%m-%Y'), time=datetime.now().strftime('%H:%M'), body=form.remarks.data, type='Maintenance'))
                db.session.commit()
                return redirect(url_for('maintenance_request_success'))
         else:
            return render_template('maintenance_request.html', form=form)
               
@app.route('/maintenance_request_success', methods=['GET', 'POST'])
@login_required
def maintenance_request_success():
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
        
        if request.method == 'POST':
            if request.form.get('maintenance_success_action') == 'Home':
                return redirect(url_for('home'))
        elif request.method == 'GET':
            return render_template('maintenance_request_success.html') 
        
@app.route('/manage_requests', methods=['GET', 'POST'])
@login_required      
def manage_requests():
         if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
         
         if request.method == 'POST':
              req=Requests.query.filter_by(id=request.form.get('manage_req_action')).first().type
              if req == 'Housekeeping':
                   return redirect(url_for('housekeeping_edit', req_edit=Requests.query.filter_by(id=request.form.get('manage_req_action')).first().id))
              elif req == 'Maintenance':
                   return redirect(url_for('maintenance_edit'))
              
         elif request.method == 'GET':
             requests=Requests.query.filter_by(ashoka_id=current_user.ashoka_id).all()
             requests.reverse()
             #requests=current_user.all_requests.all()[0]
             return render_template('manage_requests_table.html', requests=requests)
         

@app.route('/housekeeping_edit/<req_edit>', methods=['GET', 'POST'])
@login_required
def housekeeping_edit(req_edit):
        if current_user.ashoka_id == 1000:
            return redirect(url_for('admin'))
        
        edit_request=Requests.query.filter_by(id=req_edit).first() 
        time=edit_request.time_slot
        text_body=edit_request.body
        
        form=HouseEditForm()
        if form.validate_on_submit():         
            edit_request.body = form.remarks.data
            edit_request.time_slot = form.time_slot.data
            db.session.commit()
            return redirect(url_for('manage_requests'))
            
        else:
            form.time_slot.data=time
            form.remarks.data=text_body      
            return render_template('housekeeping_edit.html', form=form)
            