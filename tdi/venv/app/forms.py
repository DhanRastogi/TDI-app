from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from flask_login import current_user

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
    #floor=SelectField('Floor', choices=[('GF','Ground Floor'),('FF','First Floor'),('SF','Second Floor'),('TF','Third Floor'),('Duplex','Duplex')],validators=[DataRequired()])
    room=IntegerField('Room Number', validators=[DataRequired()])
    submit=SubmitField('Continue')  

    def validate_ashoka_email(self, ashoka_email):
        user = User.query.filter_by(ashoka_id=ashoka_email.data).first()
        if user is not None:
            raise ValidationError('Ashoka ID already exists')
        

class LogInForm(FlaskForm):
    ashoka_id=IntegerField('Ashoka ID', validators=[DataRequired()])  
    password=PasswordField('Password', validators=[DataRequired()])
    remember_me=BooleanField('Remember Me')
    submit=SubmitField('Sign In')
    register=SubmitField('Register Here')

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ashoka_email=StringField('Ashoka Email', validators=[DataRequired(), Email()])
    ashoka_id=IntegerField('Ashoka ID', validators=[DataRequired()]) 
    flat=IntegerField('Flat Number', validators=[DataRequired()])
    room=IntegerField('Room Number', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_ashoka_id(self, ashoka_id):
        user = User.query.filter_by(ashoka_id=ashoka_id.data).all()
        if current_user not in user:
            raise ValidationError('Ashoka ID already exists')
        
    def validate_ashoka_email(self, ashoka_email):
        user = User.query.filter_by(ashoka_email=ashoka_email.data).all()
        if current_user not in user:
            raise ValidationError('Ashoka email already exists')


class MealForm(FlaskForm):
    meal_date=DateField('Date')
    book=SubmitField('Book')

#class HouseForm(FlaskForm):
    #house_time=SelectField('Time Slot', choices=[('8 - 9'), ('9 - 10'), ('10 - 11'), ('11 - 12'), ('12 - 1'), ('2 - 3'), ('3 - 4'), ('4 - 5')])
    #remarks=TextAreaField('Remarks')
    #submit=SubmitField('Submit')



                         