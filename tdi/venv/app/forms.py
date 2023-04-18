from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from flask_login import current_user
from datetime import datetime

class LogInForm(FlaskForm):
    ashoka_id=IntegerField('Ashoka ID', validators=[DataRequired()])  
    password=PasswordField('Password', validators=[DataRequired()])
    remember_me=BooleanField('Remember Me')
    submit=SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    #ashoka_email = StringField('Ashoka Email ID', validators=[DataRequired(), Email()])
    ashoka_id = IntegerField('Ashoka ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_ashoka_id(self, ashoka_id):
        user = User.query.filter_by(ashoka_id=ashoka_id.data).first()
        if user is not None:
            raise ValidationError('Ashoka ID already exists')
        
        
class UserDetailsForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    ashoka_email=StringField('Ashoka Email', validators=[DataRequired(), Email()])    
    flat=IntegerField('Flat Number', validators=[DataRequired()])
    floor=SelectField('Floor', choices=[('GF','Ground Floor'),('FF','First Floor'),('SF','Second Floor'),('TF','Third Floor'),('Duplex','Duplex')],validators=[DataRequired()])
    room=IntegerField('Room Number', validators=[DataRequired()])
    submit=SubmitField('Continue')  

    def validate_ashoka_email(self, ashoka_email):
        user = User.query.filter_by(ashoka_email=ashoka_email.data).first()
        if user is not None:
            raise ValidationError('Email already exists')
        

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ashoka_email=StringField('Ashoka Email', validators=[DataRequired(), Email()])
    ashoka_id=IntegerField('Ashoka ID', validators=[DataRequired()]) 
    flat=IntegerField('Flat Number', validators=[DataRequired()])
    floor=SelectField('Floor', choices=[('GF','Ground Floor'),('FF','First Floor'),('SF','Second Floor'),('TF','Third Floor'),('Duplex','Duplex')],validators=[DataRequired()])
    room=IntegerField('Room Number', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_ashoka_id(self, ashoka_id):
        user = User.query.filter_by(ashoka_id=ashoka_id.data).all()
        if current_user in user:
            user.remove(current_user)
        if len(user)!=0:
            raise ValidationError('Ashoka ID already exists')
        
    def validate_ashoka_email(self, ashoka_email):
        user_mail = User.query.filter_by(ashoka_email=ashoka_email.data).all()
        if current_user in user_mail:
            user_mail.remove(current_user)
        if len(user_mail)!=0:
            raise ValidationError('Ashoka email already exists')


class MealForm(FlaskForm):
    meal_date=DateField('Date')
    book=SubmitField('Book')

class HouseForm(FlaskForm):
    slots=['9 am - 10 am', '10 am - 11 am', '11 am - 12 pm', '12 pm - 1 pm', '1 pm - 2 pm', '3 pm - 4 pm', '4 pm - 5 pm']
    now=datetime.now().strftime('%H:%M:%S')
    now_time=datetime.strptime(now,'%H:%M:%S')
    choices=[]
    if now_time > datetime.strptime('15:45:00','%H:%M:%S'):
        cutoff='9 am - 10 am'
    elif now_time > datetime.strptime('14:45:00','%H:%M:%S'):
        cutoff='10 pm - 11 pm'
    elif now_time > datetime.strptime('12:45:00','%H:%M:%S'):   
        cutoff='11 am - 12 pm'
    elif now_time > datetime.strptime('11:45:00','%H:%M:%S'): 
        cutoff='12 pm - 1 pm'
    elif now_time > datetime.strptime('10:45:00','%H:%M:%S'):
        cutoff='1 pm - 2 pm'
    elif now_time > datetime.strptime('09:45:00','%H:%M:%S'):
        cutoff='3 pm - 4 pm'
    elif now_time > datetime.strptime('08:45:00','%H:%M:%S'):
        cutoff='4 pm - 5 pm'
    cutoff

    for i in range(0,slots.index(cutoff)):
        choices+=[(slots[i], slots[i])]

    time_slot=SelectField('Time Slot', choices=choices+[('ASAP','ASAP')], validators=[DataRequired()])
    remarks=TextAreaField('Remarks')
    submit=SubmitField('Submit')

class MaintenanceForm(FlaskForm):
    remarks=TextAreaField('Remarks')
    book=SubmitField('Book')

class HouseEditForm(FlaskForm):
    slots=['9 am - 10 am', '10 am - 11 am', '11 am - 12 pm', '12 pm - 1 pm', '1 pm - 2 pm', '3 pm - 4 pm', '4 pm - 5 pm']
    now=datetime.now().strftime('%H:%M:%S')
    now_time=datetime.strptime(now,'%H:%M:%S')
    choices=[]
    if now_time > datetime.strptime('15:45:00','%H:%M:%S'):
        cutoff='9 am - 10 am'
    elif now_time > datetime.strptime('14:45:00','%H:%M:%S'):
        cutoff='10 pm - 11 pm'
    elif now_time > datetime.strptime('12:45:00','%H:%M:%S'):   
        cutoff='11 am - 12 pm'
    elif now_time > datetime.strptime('11:45:00','%H:%M:%S'): 
        cutoff='12 pm - 1 pm'
    elif now_time > datetime.strptime('10:45:00','%H:%M:%S'):
        cutoff='1 pm - 2 pm'
    elif now_time > datetime.strptime('09:45:00','%H:%M:%S'):
        cutoff='3 pm - 4 pm'
    elif now_time > datetime.strptime('08:45:00','%H:%M:%S'):
        cutoff='4 pm - 5 pm'
    cutoff

    for i in range(0,slots.index(cutoff)):
        choices+=[(slots[i], slots[i])]

    time_slot=SelectField('Time Slot', choices=choices+[('ASAP','ASAP')], validators=[DataRequired()])
    remarks=TextAreaField('Remarks')
    submit=SubmitField('Modify')